create table if not exists public.incident_notes (
  id uuid primary key default gen_random_uuid(),
  incident_id uuid not null references public.incidents(id) on delete cascade,
  note_type text not null check (note_type in ('triage')),
  content text not null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create unique index if not exists idx_incident_notes_unique on public.incident_notes(incident_id, note_type);
create index if not exists idx_incident_notes_incident_updated on public.incident_notes(incident_id, updated_at desc);

alter table public.incident_notes disable row level security;
grant select, insert, update, delete on public.incident_notes to anon, authenticated;
