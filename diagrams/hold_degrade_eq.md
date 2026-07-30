# Hold/degrade (simple accounting)

For suite size \(N = 5\) cases D01–D05:

\[
\text{hold} = \#\{i : \text{home}_i=\text{PASS} \land \text{open}_i=\text{PASS}\}
\]

\[
\text{degrade} = \#\{i : \text{home}_i=\text{PASS} \land \text{open}_i=\text{FAIL}\}
\]

\[
\text{improve} = \#\{i : \text{home}_i=\text{FAIL} \land \text{open}_i=\text{PASS}\}
\]

Report rates \(\text{hold}/N\), \(\text{degrade}/N\). Label each non-hold with layer: model · instructions · tests · environment · brief.
