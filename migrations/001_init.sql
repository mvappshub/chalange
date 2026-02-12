create extension if not exists pgcrypto;

create table if not exists public.cards (
  id uuid primary key default gen_random_uuid(),
  title text not null check (char_length(title) >= 2),
  description text not null default '',
  column_name text not null check (column_name in ('Todo', 'In Progress', 'Done')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.alerts (
  id uuid primary key default gen_random_uuid(),
  title text not null check (char_length(title) >= 3),
  severity text not null check (severity in ('low', 'medium', 'high', 'critical')),
  source text not null default 'manual',
  status text not null default 'open',
  escalated boolean not null default false,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.incidents (
  id uuid primary key default gen_random_uuid(),
  title text not null,
  status text not null check (status in ('investigating', 'mitigated', 'resolved')),
  severity text not null check (severity in ('high', 'critical')),
  source_alert_id uuid null references public.alerts(id) on delete set null,
  summary text not null default '',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.audit_events (
  id uuid primary key default gen_random_uuid(),
  action text not null,
  entity_type text not null,
  entity_id text not null,
  payload jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

alter table public.cards disable row level security;
alter table public.alerts disable row level security;
alter table public.incidents disable row level security;
alter table public.audit_events disable row level security;

grant usage on schema public to anon, authenticated;
grant select, insert, update, delete on public.cards to anon, authenticated;
grant select, insert, update, delete on public.alerts to anon, authenticated;
grant select, insert, update, delete on public.incidents to anon, authenticated;
grant select, insert, update, delete on public.audit_events to anon, authenticated;
