# How to use the final presentation template

Your team presents on Day 2 (Wed Oct 14) from 9:40 AM, in order 01 → 04, for about 20 minutes, give or take, including a few questions. Grok Bot builds the deck for you from what you did; you check it and present.

1. **Download the template.** Get [AI-in-Action-Final-Presentation-Template.pptx](template/AI-in-Action-Final-Presentation-Template.pptx) and the [agent instructions](final-presentation-agent-instructions.md). Glance at the [preview](template/template-contact-sheet.jpg): 13 slides in the keynote's style, with [brackets] where your content goes.

2. **Keep your capture log during the hack.** On Day 1 at about 2:10 PM, paste the box from the agent instructions into your team's Grok Bot conversation. From then on, Grok Bot keeps a [capture log](capture-log-template.md) of your decisions, before and after workflows, prompts, swarm, human gates, screenshots and timings. Say "log that" when something matters, upload screenshots of the runs, and give it your own impact estimates. There is no formal share-out at the end of Day 1.

3. **Give Grok Bot the template, the agent instructions and your capture log.** On Day 2 at about 9:05 AM, upload all three and paste this prompt:

   ```text
   Build our final presentation for AI in Action for Medical Affairs.
   Attached: the template (AI-in-Action-Final-Presentation-Template.pptx), the agent instructions
   (final-presentation-agent-instructions.md) and our capture log (capture-log.md).
   Follow PART 2 of the agent instructions exactly:
   - open the template and keep its layouts; read the FOR THE AGENT notes on each slide;
   - fill every slide from our capture log; leave slide 7 (LIVE DEMO) empty except our team name;
   - build the impact chart from OUR estimates only, and never invent a number, name or source;
   - mark the practice data as fictional;
   - check that no [bracket] is left, render the slides and review them;
   - then give us the .pptx and a slide-by-slide summary to approve.
   Team: [team name] · Vertical: [01 Publications Brain | 02 Insights Engine | 03 Congress Monitor | 04 Field Intelligence Engine]
   ```

4. **Review and edit.** Read every slide and its speaker notes. Check that there are no [brackets] left, the numbers are your team's own estimates, the practice data are marked fictional, and nothing confidential slipped in. Tell Grok Bot what to change, or edit the .pptx yourselves. It is final only when your team says so.

5. **Leave the demo slide empty and run the live demo there.** Slide 7 says LIVE DEMO and nothing else, on purpose. When you reach it, switch to your Grok Bot conversation and run the swarm live: the assignment, the plan, the hand-offs, the human gate (decide out loud), the output. If the live run fails, go to slide 8 (Backup) and show your screenshots.

6. **Present in about 20 minutes.** Rehearse once with a timer, give or take a minute or two, and leave time for a few questions. Hand the final .pptx to the presentation laptop before 9:38 AM.

*Practice data are fictional (Nordvant Biopharma; NORVANTIB, DERMALYX, ADIPOSYN). Outputs are drafts for qualified human review.*
