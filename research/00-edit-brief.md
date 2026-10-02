# Line-edit brief: take the mannerism out

Rob read the tracks on his phone and found them "punchy, fatiguing, mannered": too much parataxis and too many stage directions. Your job is a line edit, not a rewrite of the content. Every fact, number, date, name, hedge and practical instruction stays. What changes is the sentence-level texture.

## Write like this

- Connected prose. Let sentences carry their logic with subordinate clauses, participles and real transitions ("because", "which is why", "by then", "after the fire"), so the reader is led rather than prodded. Vary length naturally; most sentences should be medium length, with an occasional long one and only a rare short one when it earns its place.
- A good guidebook or essayist register: knowledgeable, unhurried, specific, quietly warm. Think of a well-read friend walking beside you, not a narrator performing.
- Hedges stated once, plainly, inside the sentence: "by local tradition", "sources give 22 or 23", "the date is disputed (about 1839 or 1864)". Not a separate sentence telling the reader what to do with it.
- Keep the second person where it orients the reader ("from the fence you can see..."), but less of it as command.

## Remove these

- Signposting and stage directions: "Start with...", "Now look at...", "Now the tree.", "Then there is...", "Here is the part that matters", "Now the part that matters for Jamie's way of looking", "Keep that in mind", "Hold on to this", "Notice...", "Look at..." as a sentence opener more than once per stop.
- Staccato runs of short declaratives and fragments: "Souda held. So did Gramvousa and Spinalonga." "The fighting was over." "Keep going." Join them into the sentences around them.
- Aphoristic button endings to paragraphs: "Fire is a good excavator." "Every faction left a layer." "The lentils never made it to dinner." "That is the plot of the whole city in one block." Either fold the idea into a fuller sentence or cut it.
- Rhetorical questions answered at once ("Who is he? A king, a god..."; "Who worked here? The sources are thin..."). State it instead.
- "That is why / That is the / That is about..." as a sentence opener; "not just X; it is Y"; colon reveals; tidy triplets for rhythm; any reference to the reader's track, to "Jamie's way of looking", or to the guide itself.
- Explicit game talk on Rob's track: at most one light, integrated D&D or campaign reference per stop, carried by imagery rather than announced ("D&D players might call this..." goes). None at the synagogue.

## Keep

- The opening that orients the reader at the spot, and the closing direction to the next stop (direction, roughly how far or how long).
- Paragraphing roughly as is (plain paragraphs separated by a blank line; no headings, lists or markdown). Digits for numbers.
- Length: each long within 10 per cent of its current word count; each short between 90 and 140 words.
- Titles may be lightly improved but needn't change.

## Output

Read your five stops from the given input file (a JSON array of all ten; edit only the slugs you're given), and write a JSON array of just your five edited objects, same keys (n, slug, title, short, long), to the given output path. Validate it with `python3 -c "import json;json.load(open(PATH))"` and report word counts before and after.
