-- Supabase/PostgreSQL starter schema.
-- Run in the Supabase SQL Editor after creating a project.
create extension if not exists pgcrypto;

create table if not exists public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  display_name text,
  created_at timestamptz not null default now()
);

create table if not exists public.watchlists (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  name text not null default 'My Watchlist',
  created_at timestamptz not null default now()
);

create table if not exists public.watchlist_items (
  id uuid primary key default gen_random_uuid(),
  watchlist_id uuid not null references public.watchlists(id) on delete cascade,
  user_id uuid not null references auth.users(id) on delete cascade,
  symbol text not null,
  market text,
  notes text,
  created_at timestamptz not null default now(),
  unique (watchlist_id, symbol)
);

create table if not exists public.saved_screens (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  name text not null,
  filters jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create table if not exists public.invitations (
  id uuid primary key default gen_random_uuid(),
  email text not null unique,
  invited_by uuid references auth.users(id) on delete set null,
  created_at timestamptz not null default now(),
  accepted_at timestamptz
);

alter table public.profiles enable row level security;
alter table public.watchlists enable row level security;
alter table public.watchlist_items enable row level security;
alter table public.saved_screens enable row level security;
alter table public.invitations enable row level security;

create policy "Users can view own profile" on public.profiles
  for select using (auth.uid() = id);
create policy "Users can update own profile" on public.profiles
  for update using (auth.uid() = id) with check (auth.uid() = id);
create policy "Users manage own watchlists" on public.watchlists
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);
create policy "Users manage own watchlist items" on public.watchlist_items
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);
create policy "Users manage own saved screens" on public.saved_screens
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

-- Invitation table is intentionally not readable by regular users.
-- Manage invitations through trusted admin/service-role tooling only.
