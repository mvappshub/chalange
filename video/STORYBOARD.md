# Demo storyboard (2-3 min)

1. **Board flow**  
   Create card -> move to `In Progress` -> open audit log and show `card_moved`.

2. **Alert flow**  
   Create `critical` alert -> run watcher once -> open incidents list.

3. **Incident timeline**  
   Open incident detail and show timeline.

4. **Monitoring**  
   Open `/monitoring` and `/metrics`.

5. **Agent flow**  
   Run `python scripts/agent_graph.py` with `INCIDENT_ID` and show new remediation cards on board.
