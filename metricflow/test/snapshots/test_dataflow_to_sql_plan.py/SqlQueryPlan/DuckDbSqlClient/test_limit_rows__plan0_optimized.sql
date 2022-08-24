-- Aggregate Measures
-- Compute Metrics via Expressions
-- Order By [] Limit 1
SELECT
  ds
  , SUM(bookings) AS bookings
FROM (
  -- Read Elements From Data Source 'bookings_source'
  -- Pass Only Additive Measures
  -- Metric Time Dimension 'ds'
  -- Pass Only Elements:
  --   ['bookings', 'ds']
  SELECT
    ds
    , 1 AS bookings
  FROM (
    -- User Defined SQL Query
    SELECT * FROM ***************************.fct_bookings
  ) bookings_source_src_10001
) subq_9
GROUP BY
  ds
LIMIT 1