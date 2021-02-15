; 
WITH 
    sal_rank AS
    (   SELECT
            concat(first_name,last_name) AS employee_name ,
            department_id,
            salary ,
            row_number() OVER (PARTITION BY  employee_id ORDER BY salary DESC) AS salary_rank
        FROM
            employees
    )
SELECT
    department_name,
    employee_name AS top_employee_name,
    salary_of_top_employee,
    SUM( 
    CASE 
        WHEN salary_rank = 1 
        THEN salary 
        ELSE -salary END) AS diff_from_second_earning
FROM 
    departments D
WHERE 
    salary_rank <=2
ORDER BY 
    salary DESC LIMIT 1;

