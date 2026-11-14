# Mascot library (reusable across episodes)

Generated 2026-11-14 on Higgsfield (nano_banana_pro, 2k) with mascot_v2 + mascot_v3a_0 as references; prompts in prompts.json, originals in raw/.
Copy the files an episode needs into its layers/ folder (the engine loads layers/<name>.jpg).

Poses (3:4, full body on flat cream, used as cut-outs): beat event `M(at, "p_name")` (named pose, waist-up framing like the numbered poses).
| name | what he does | fits |
|---|---|---|
| p_basket | shopping basket, surprised | prices, groceries, inflation |
| p_banknotes | fans a stack of banknotes, pleased | money, salary, cash |
| p_empty_wallet | empty wallet upside down, coin falling | losing money, poverty, prices |
| p_calculator | calculator, pencil behind ear | maths, budgets, real value |
| p_receipt | very long receipt, shocked | bills, price rises |
| p_gold | gold bar, admiring | gold, savings, reserves |
| p_piggy | hugs a piggy bank, worried | savings, deposits |
| p_pointer | pointer stick, teacher | "3 reasons", explaining lists |
| p_book | reads an old history book | history, background |
| p_globe | small globe (globe is coloured: off palette, use sparingly) | world, countries |
| p_scale | balance scale, weighing | debates, pros and cons |
| p_newspaper | reads a newspaper, shocked | news, expectations, headlines |

Scenes (16:9, mascot in the left third, right half calm for tags): use as `bg` of a scene beat; keep tags on the right (default column).
| name | where | fits |
|---|---|---|
| s_bazaar | Tashkent bazaar stall, looks at a price tag | prices, everyday life |
| s_kitchen | kitchen table with receipts, calculator, piyola | family budget, questions |
| s_bank | bank counter with a teller, piggy bank | deposits, loans, banks |
| s_exchange | exchange office rate board, banknotes | currency, exchange rate, dollar |
| s_library | library, open book | history, research, "who am I" |
| s_office | flipchart with a rising chart | explaining data, growth |
| s_vault | bank vault with gold bars | gold, reserves, central banks |
| s_street | Tashkent street with shopping bags, tired | cost of living |

Add new ones the same way (same prompt prefix, both references) when an episode needs a situation that isn't here, and list them in this table.
