# Module 02 — Control context and reusable instructions

**Serves oracle:** S04, S07, S09, S14, S18, S19  
**Primary objective:** PO-02 — Control context and reusable instructions  
**Prerequisites:** Preflighted accessible environment and this module's supplied case  
**Consumes:** VERIFY:PREFLIGHT; VERIFY:CASE; VERIFY:PROTECTED_GUARD  
**Produces:** CONTEXT_MAP; SOURCE_AS_DATA_CONTROL; RELOAD_RESULT; PO02_RESULT  
**Facilitated time:** 3 hours  
**Practice time:** 2 hours  
**Performance stage:** Independent  
**Work surface:** Reusable instruction and guard  
**Practical work:** Confirm the supplied protected guard, map resolved harness state for the supplied case, place one recurring rule in a saved instruction and one material condition in that guard, then test precedence, loading, reset survival, and bypass.  
**Performance evidence:** CONTEXT_MAP, independent matched precedence result, SOURCE_AS_DATA_CONTROL, protected guard results on an allowed case and a material negative, RELOAD_RESULT, and bounded bypass evidence.  
**Failure / HOLD:** Hold when no supplied protected guard exists, resolved state is unobservable, the producer can edit or select the guard, reset conditions cannot be stated, or instruction-like source content gains trusted precedence.  
**Scope boundary:** Proves control placement and restartability in the tested harness for bounded internal use; it does not authorize consequential release or tool effects, or prove portability to another product.  
**Handoff:** Give the next owner the context map, the saved rule and its guard, the reload action, and the remaining bypass risk.

## Why

More prompt text is not a durable control. An operator has to tell the difference between temporary advice, saved advice, deterministic enforcement, and authority — and prove which of them actually loaded.

## Enabling objectives

1. Map direction, sources, instructions, tools, permissions, state, feedback, and decisive evidence from resolved views.
2. Test one factor where instruction-like untrusted source content must remain data.
3. Distinguish not loaded, not triggered, failed execution, and executed but bypassed.

## Gate

Pass PO-02 when the learner predicts the matched behavior and the protected result confirms it, SOURCE_AS_DATA_CONTROL holds untrusted content as data, the saved instruction is observed after a clean reload, the guard accepts an allowed case and rejects a material negative, and remaining bypass conditions are stated rather than hidden. No consequential release is claimed.
