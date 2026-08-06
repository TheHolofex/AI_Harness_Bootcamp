import csv
import json
import re
import shutil
import subprocess
import tempfile
import unittest
import xml.etree.ElementTree as ET
import zipfile
from datetime import datetime
from pathlib import Path


P7 = Path(__file__).resolve().parents[1]
INPUT_FIELDS = ["id", "received_at", "requester", "channel", "text", "wave"]
WORKBOARD_FIELDS = [
    "id",
    "received_at",
    "requester",
    "channel",
    "text",
    "wave",
    "workstream",
    "priority",
    "summary",
    "next_action",
    "branch_policy",
    "policy_value",
    "sla_hours",
    "target_by",
]
POLICY_NODES = [
    "POLICY — Operations SLA 24h",
    "POLICY — Finance owner + evidence",
    "POLICY — People owner + private channel",
    "POLICY — Technology triage + incident link",
]


def read_csv(name):
    with (P7 / "inputs" / name).open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames, list(reader)


def workflow():
    return json.loads(
        (P7 / "workflow" / "P7-production-line.template.json").read_text(
            encoding="utf-8"
        )
    )


def by_name(data):
    return {node["name"]: node for node in data["nodes"]}


def workbook_shape(name):
    path = P7 / "inputs" / name
    with zipfile.ZipFile(path) as archive:
        workbook_xml = ET.fromstring(archive.read("xl/workbook.xml"))
        sheet_xml = ET.fromstring(archive.read("xl/worksheets/sheet1.xml"))
        table_xml = ET.fromstring(archive.read("xl/tables/table1.xml"))

    main = {"x": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    sheet_names = [node.attrib["name"] for node in workbook_xml.findall(".//x:sheet", main)]
    rows = sheet_xml.findall(".//x:sheetData/x:row", main)
    header = []
    for cell in rows[0].findall("x:c", main):
        value = cell.find("x:v", main)
        header.append("" if value is None else value.text)
    first_data_cells = {}
    for cell in rows[1].findall("x:c", main):
        value = cell.find("x:v", main)
        first_data_cells[cell.attrib["r"]] = None if value is None else value.text
    return {
        "path": path,
        "sheet_names": sheet_names,
        "rows": len(rows),
        "header": header,
        "first_data_cells": first_data_cells,
        "table_ref": table_xml.attrib["ref"],
    }


class SourceFixtureTests(unittest.TestCase):
    def test_wave_counts_fields_and_ids(self):
        wave1_fields, wave1 = read_csv("wave1.csv")
        wave2_fields, wave2 = read_csv("wave2.csv")
        self.assertEqual(INPUT_FIELDS, wave1_fields)
        self.assertEqual(INPUT_FIELDS, wave2_fields)
        self.assertEqual(60, len(wave1))
        self.assertEqual(20, len(wave2))
        self.assertEqual({"1"}, {row["wave"] for row in wave1})
        self.assertEqual({"2"}, {row["wave"] for row in wave2})
        all_rows = wave1 + wave2
        self.assertEqual(
            [f"INT-{number:03d}" for number in range(1, 81)],
            [row["id"] for row in all_rows],
        )
        self.assertEqual(80, len({row["id"] for row in all_rows}))

    def test_source_rows_are_complete_and_timestamps_parse(self):
        rows = read_csv("wave1.csv")[1] + read_csv("wave2.csv")[1]
        for row in rows:
            for field in INPUT_FIELDS:
                self.assertTrue(row[field].strip(), f"{row['id']} missing {field}")
            datetime.fromisoformat(row["received_at"])
            self.assertIn(row["channel"], {"email", "slack", "portal", "phone"})
            self.assertGreaterEqual(len(row["text"].split()), 8)


class WorkbookFixtureTests(unittest.TestCase):
    def test_blank_workbooks_have_exact_sheet_headers_and_row_counts(self):
        for name, source_rows in [
            ("workboard_60_blank.xlsx", 60),
            ("workboard_80_blank.xlsx", 80),
        ]:
            shape = workbook_shape(name)
            self.assertGreater(shape["path"].stat().st_size, 10_000)
            self.assertEqual(["AI Workboard"], shape["sheet_names"])
            self.assertEqual(source_rows + 1, shape["rows"])
            self.assertEqual(WORKBOARD_FIELDS, shape["header"])
            self.assertEqual(f"A1:N{source_rows + 1}", shape["table_ref"])

    def test_blank_workbooks_populate_source_cells_and_leave_ai_cells_blank(self):
        for name in ["workboard_60_blank.xlsx", "workboard_80_blank.xlsx"]:
            cells = workbook_shape(name)["first_data_cells"]
            for column in "ABCDEF":
                self.assertIsNotNone(cells[f"{column}2"], f"{name} {column}2 is blank")
            for column in "GHIJKLMN":
                self.assertIsNone(cells[f"{column}2"], f"{name} {column}2 is populated")


class WorkflowShapeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = workflow()
        cls.nodes = by_name(cls.data)

    def test_import_envelope_and_unique_nodes(self):
        self.assertEqual("P7 — AI Controls the Workboard", self.data["name"])
        self.assertEqual("P7SpreadsheetControl01", self.data["id"])
        self.assertFalse(self.data["active"])
        self.assertEqual("v1", self.data["settings"]["executionOrder"])
        self.assertEqual(len(self.data["nodes"]), len(self.nodes))
        self.assertEqual(
            len(self.data["nodes"]), len({node["id"] for node in self.data["nodes"]})
        )

    def test_local_workbook_read_and_extract_settings(self):
        reader = self.nodes["Read workboard.xlsx"]
        self.assertEqual("n8n-nodes-base.readWriteFile", reader["type"])
        self.assertEqual("__P7_WORKBOARD__", reader["parameters"]["fileSelector"])
        self.assertEqual("data", reader["parameters"]["options"]["dataPropertyName"])

        extractor = self.nodes["Extract AI Workboard sheet"]
        self.assertEqual("n8n-nodes-base.extractFromFile", extractor["type"])
        self.assertEqual("xlsx", extractor["parameters"]["operation"])
        self.assertEqual("data", extractor["parameters"]["binaryPropertyName"])
        self.assertEqual("AI Workboard", extractor["parameters"]["options"]["sheetName"])
        self.assertTrue(extractor["parameters"]["options"]["headerRow"])
        self.assertTrue(extractor["parameters"]["options"]["includeEmptyCells"])

        map_code = self.nodes["Map Spreadsheet Rows"]["parameters"]["jsCode"]
        self.assertIn("value - 25569", map_code)
        self.assertIn("Spreadsheet row", map_code)

    def test_ai_grouping_model_and_structured_contract(self):
        group_code = self.nodes["Group into 5-Record Model Calls"]["parameters"]["jsCode"]
        self.assertIn("RECORDS_PER_MODEL_CALL = 5", group_code)
        self.assertIn("change 5 to 10", group_code)

        ai = self.nodes["AI Structure Station"]
        self.assertEqual("@n8n/n8n-nodes-langchain.chainLlm", ai["type"])
        self.assertEqual(1.9, ai["typeVersion"])
        self.assertEqual(
            {"batchSize": 3, "delayBetweenBatches": 400},
            ai["parameters"]["batching"],
        )

        model = self.nodes["xAI Model — attach credential here"]
        self.assertEqual("__P7_MODEL__", model["parameters"]["model"])
        self.assertEqual(
            {"temperature": 0, "maxTokens": 1200, "timeout": 360000, "maxRetries": 2},
            model["parameters"]["options"],
        )
        self.assertNotIn("credentials", model)

        schema = json.loads(
            self.nodes["Structured Output Contract"]["parameters"]["inputSchema"]
        )
        record_schema = schema["properties"]["records"]["items"]
        self.assertEqual(
            ["OPERATIONS", "FINANCE", "PEOPLE", "TECHNOLOGY"],
            record_schema["properties"]["workstream"]["enum"],
        )
        self.assertEqual(
            ["P1", "P2", "P3"],
            record_schema["properties"]["priority"]["enum"],
        )

    def test_merge_route_four_policies_and_fan_in(self):
        merge = self.nodes["Merge Source + AI by ID"]
        self.assertEqual("id", merge["parameters"]["fieldsToMatchString"])
        self.assertEqual("enrichInput1", merge["parameters"]["joinMode"])

        route = self.nodes["Route by Workstream"]
        self.assertEqual(4, route["parameters"]["numberOutputs"])
        self.assertIn("OPERATIONS: 0", route["parameters"]["output"])
        route_outputs = self.data["connections"]["Route by Workstream"]["main"]
        self.assertEqual(POLICY_NODES, [output[0]["node"] for output in route_outputs])

        fan_in = self.nodes["Fan In — AI Workboard"]
        self.assertEqual("append", fan_in["parameters"]["mode"])
        self.assertEqual(4, fan_in["parameters"]["numberInputs"])
        fan_inputs = set()
        for policy in POLICY_NODES:
            edge = self.data["connections"][policy]["main"][0][0]
            self.assertEqual("Fan In — AI Workboard", edge["node"])
            fan_inputs.add(edge["index"])
        self.assertEqual({0, 1, 2, 3}, fan_inputs)

    def test_operations_policy_is_one_line_edit_and_observable(self):
        policy = self.nodes["POLICY — Operations SLA 24h"]["parameters"]["jsCode"]
        self.assertIn("const OPERATIONS_SLA_HOURS = 24", policy)
        self.assertIn("change 24 to 8", policy)
        for field in ["branch_policy", "policy_value", "sla_hours", "target_by"]:
            self.assertIn(field, policy)

    def test_workbook_writeback_and_verifier_outputs(self):
        builder = self.nodes["Build AI Workboard rows"]
        for field in WORKBOARD_FIELDS:
            self.assertIn(f'"{field}"', builder["parameters"]["jsCode"])

        converter = self.nodes["Convert rows to workboard.xlsx"]
        self.assertEqual("xlsx", converter["parameters"]["operation"])
        self.assertEqual("AI Workboard", converter["parameters"]["options"]["sheetName"])
        self.assertTrue(converter["parameters"]["options"]["headerRow"])
        self.assertEqual("workboard.xlsx", converter["parameters"]["options"]["fileName"])

        writer = self.nodes["Write workboard.xlsx — close Excel first"]
        self.assertEqual("__P7_WORKBOARD__", writer["parameters"]["fileName"])
        self.assertEqual("data", writer["parameters"]["dataPropertyName"])

        mirror = self.nodes["Write AI_workboard.csv"]
        receipt = self.nodes["Write run_receipt.json"]
        self.assertEqual(
            "__P7_OUTPUT_DIR__/AI_workboard.csv", mirror["parameters"]["fileName"]
        )
        self.assertEqual(
            "__P7_OUTPUT_DIR__/run_receipt.json", receipt["parameters"]["fileName"]
        )

        fan_outputs = {
            edge["node"]
            for edge in self.data["connections"]["Fan In — AI Workboard"]["main"][0]
        }
        self.assertEqual({"Build AI Workboard rows", "Build Run Receipt"}, fan_outputs)

    def test_workflow_contains_no_old_bundle_architecture_or_secret(self):
        serialized = json.dumps(self.data).lower()
        for forbidden in [
            "master_register",
            "queue_operations",
            "queue_finance",
            "queue_people",
            "queue_technology",
            "workload_snapshot",
            "current.csv",
            "xai-",
            "api_key",
            "poison",
            "human gate",
        ]:
            self.assertNotIn(forbidden, serialized)

    def test_all_code_node_javascript_parses(self):
        node_binary = shutil.which("node")
        if not node_binary:
            self.skipTest("Node.js is not installed")
        code_nodes = [
            node
            for node in self.data["nodes"]
            if node["type"] == "n8n-nodes-base.code"
        ]
        with tempfile.TemporaryDirectory() as temp_dir:
            for index, code_node in enumerate(code_nodes):
                path = Path(temp_dir) / f"node-{index}.js"
                path.write_text(code_node["parameters"]["jsCode"], encoding="utf-8")
                result = subprocess.run(
                    [node_binary, "--check", str(path)],
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(
                    0,
                    result.returncode,
                    f"{code_node['name']} JavaScript failed to parse: {result.stderr}",
                )


class HelperContractTests(unittest.TestCase):
    def test_three_expected_powershell_helpers_exist(self):
        expected = ["Add-P7Wave2.ps1", "Prepare-P7.ps1", "Verify-P7.ps1"]
        self.assertEqual(
            expected, sorted(path.name for path in (P7 / "scripts").glob("*.ps1"))
        )

    def test_prepare_creates_active_workbook_and_generated_workflow(self):
        text = (P7 / "scripts" / "Prepare-P7.ps1").read_text(encoding="utf-8")
        for marker in [
            "workboard_60_blank.xlsx",
            "workboard.xlsx",
            "P7-production-line.template.json",
            "P7-production-line.json",
            "__P7_WORKBOARD__",
            "__P7_OUTPUT_DIR__",
            "__P7_MODEL__",
            "N8N_RESTRICT_FILE_ACCESS_TO",
            "P7 WAVE 1 READY: 60 records",
            "AI_workboard.csv",
            "run_receipt.json",
            "workboard_24h.xlsx",
        ]:
            self.assertIn(marker, text)
        self.assertNotIn("Remove-Item -Recurse", text)

    def test_wave2_helper_replaces_with_immutable_80_row_workbook(self):
        text = (P7 / "scripts" / "Add-P7Wave2.ps1").read_text(encoding="utf-8")
        self.assertIn("workboard_80_blank.xlsx", text)
        self.assertIn("Copy-Item", text)
        self.assertIn("P7 WAVE 2 READY: 80 records", text)
        self.assertNotIn("Export-Csv", text)
        self.assertNotIn("-Append", text)

    def test_verifier_checks_sheet_mirror_schema_policies_and_receipt(self):
        text = (P7 / "scripts" / "Verify-P7.ps1").read_text(encoding="utf-8")
        for marker in [
            "PASS products",
            "PASS source fixtures",
            "PASS AI Workboard",
            "PASS workstream routing",
            "PASS Operations policy",
            "PASS branch policies",
            "PASS run receipt",
            "P7 SPREADSHEET CONTROL VERIFIED",
            "AI_workboard.csv",
            "workboard.xlsx",
            "run_receipt.json",
        ]:
            self.assertIn(marker, text)
        for field in WORKBOARD_FIELDS:
            self.assertIn(f"'{field}'", text)
        self.assertRegex(text, re.escape("$operationsSlaHours -eq 24"))
        self.assertRegex(text, re.escape("$operationsSlaHours -eq 8"))
        self.assertIn("unexpected non-Operations SLA", text)
        self.assertIn("unexpected non-Operations target_by", text)

    def test_template_placeholders_match_prepare_replacements(self):
        template = (P7 / "workflow" / "P7-production-line.template.json").read_text(
            encoding="utf-8"
        )
        prepare = (P7 / "scripts" / "Prepare-P7.ps1").read_text(encoding="utf-8")
        for placeholder in [
            "__P7_WORKBOARD__",
            "__P7_OUTPUT_DIR__",
            "__P7_MODEL__",
        ]:
            self.assertIn(placeholder, template)
            self.assertIn(placeholder, prepare)


if __name__ == "__main__":
    unittest.main()
