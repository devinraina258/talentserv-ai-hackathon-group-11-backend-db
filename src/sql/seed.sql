-- Employees: devin, nisha, gautam
INSERT OR IGNORE INTO employees (slug, display_name, department, email) VALUES
  ('devin', 'Devin', 'Engineering', 'devin@office.local'),
  ('nisha', 'Nisha', 'Product', 'nisha@office.local'),
  ('gautam', 'Gautam', 'Operations', 'gautam@office.local');

INSERT OR IGNORE INTO leave_balances (employee_id, annual_remaining, sick_remaining)
SELECT id, 12.0, 5.0 FROM employees WHERE slug = 'devin';

INSERT OR IGNORE INTO leave_balances (employee_id, annual_remaining, sick_remaining)
SELECT id, 10.0, 4.0 FROM employees WHERE slug = 'nisha';

INSERT OR IGNORE INTO leave_balances (employee_id, annual_remaining, sick_remaining)
SELECT id, 14.0, 6.0 FROM employees WHERE slug = 'gautam';

-- Sample approved past leave (one per employee for demo status checks)
INSERT INTO leave_requests (employee_id, leave_type, start_date, end_date, days, reason, status, created_at, updated_at)
SELECT e.id, 'annual', '2026-04-01', '2026-04-02', 2.0, 'Family visit', 'approved', datetime('now'), datetime('now')
FROM employees e WHERE e.slug = 'devin'
  AND NOT EXISTS (SELECT 1 FROM leave_requests lr WHERE lr.employee_id = e.id);

INSERT INTO leave_requests (employee_id, leave_type, start_date, end_date, days, reason, status, created_at, updated_at)
SELECT e.id, 'sick', '2026-03-10', '2026-03-10', 1.0, 'Medical appointment', 'approved', datetime('now'), datetime('now')
FROM employees e WHERE e.slug = 'nisha'
  AND (SELECT COUNT(*) FROM leave_requests lr WHERE lr.employee_id = e.id) < 2;

INSERT INTO leave_requests (employee_id, leave_type, start_date, end_date, days, reason, status, created_at, updated_at)
SELECT e.id, 'annual', '2026-02-14', '2026-02-16', 3.0, 'Personal time', 'approved', datetime('now'), datetime('now')
FROM employees e WHERE e.slug = 'gautam'
  AND (SELECT COUNT(*) FROM leave_requests lr WHERE lr.employee_id = e.id) < 2;
