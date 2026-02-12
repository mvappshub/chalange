create index if not exists idx_cards_column_name on public.cards(column_name);
create index if not exists idx_alerts_severity_escalated on public.alerts(severity, escalated);
create index if not exists idx_incidents_status_created_at on public.incidents(status, created_at desc);
create index if not exists idx_audit_entity_created_at on public.audit_events(entity_id, created_at desc);
create index if not exists idx_audit_action_created_at on public.audit_events(action, created_at desc);
