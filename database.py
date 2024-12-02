import sqlalchemy
from sqlalchemy import create_engine, text
import pymysql  # or mysql.connector for mysql-connector-python
from functools import lru_cache
from measurement import TimeMeasurement


DATABASE_URL = "mysql+pymysql://root:strong_password@mysql:3306/test_db"
DEFAULT_POOL_SIZE = 1
DEFAULT_MAX_OVERFLOW = 0
DEFAULT_POOL_TIMEOUT = 60

@lru_cache(maxsize=1)
def get_database():
    # Create the SQLAlchemy engine with connection pooling
    engine = create_engine(
        DATABASE_URL,
        pool_size=DEFAULT_POOL_SIZE,
        max_overflow=DEFAULT_MAX_OVERFLOW,
        pool_timeout=DEFAULT_POOL_TIMEOUT,
        pool_pre_ping=True
    )

    # Test the connection by executing a simple query
    return engine
        

def __generate_fibonacci(n, fib_sequence=None):
    """
    Generate Fibonacci sequence up to the nth term using recursion.
    """
    if fib_sequence is None:
        fib_sequence = [(1,1)]  # Initialize the sequence starting with the first Fibonacci number
    
    if len(fib_sequence) == n:
        return fib_sequence
    
    if len(fib_sequence) == 1:
        fib_sequence.append((2,1))  # Add the second Fibonacci number

    # Calculate the next Fibonacci number
    fib_sequence.append((len(fib_sequence)+1,fib_sequence[-1][1] + fib_sequence[-2][1]))

    return __generate_fibonacci(n, fib_sequence)

def generate_fibonacci(n):
    time_measurement = TimeMeasurement()
    time_measurement.start()
    fib_sequence = __generate_fibonacci(n)
    time_measurement.end()
    return time_measurement, fib_sequence




def __generate_fibonacci_with_sql(connection, start_n, n,iteration=1,initial_sequence=None):
    """
    Generate Fibonacci sequence using SQL starting from initial_sequence from input.
    
    Parameters:
    - connection: Database connection object
    - initial_sequence: List containing two initial Fibonacci numbers [a, b]. Defaults to [0, 0] if empty.
    - start_n: Included starting number (1-based index)
    - n: Included ending number (1-based index)
    """
    # Handle empty initial_sequence by providing default values
    if not initial_sequence:
        initial_sequence = [0, 0]
    
    # Extract the initial numbers
    a, b = initial_sequence

    # Build the SQL query using a recursive CTE
    query = text(f"""
    WITH RECURSIVE fib_sequence (iteration, n, last_2, last_1, current) AS (
        -- Base case: Start with the initial Fibonacci values
        SELECT 
            1 AS iteration,
            :start_n AS n, 
            :a AS last_2, 
            :b AS last_1, 
            CASE 
                WHEN :start_n = 1 THEN 1
                WHEN :start_n = 2 THEN 1
                ELSE :a + :b
            END AS current
        UNION ALL
        -- Recursive case: Continue Fibonacci or reset for new iteration
        SELECT 
            CASE 
                WHEN n + 1 > :n THEN iteration + 1 -- Increment iteration when sequence reaches end
                ELSE iteration 
            END AS iteration,
            CASE 
                WHEN n + 1 > :n THEN :start_n -- Reset n when moving to a new iteration
                ELSE n + 1 -- Increment n within the current iteration
            END AS n,
            CASE 
                WHEN n + 1 > :n THEN :a -- Reset last_2 to the initial value when moving to a new iteration
                ELSE last_1 -- Update Fibonacci values within the current iteration
            END AS last_2,
            CASE 
                WHEN n + 1 > :n THEN :b -- Reset last_1 to the initial value when moving to a new iteration
                ELSE current -- Update Fibonacci values within the current iteration
            END AS last_1,
            CASE 
                WHEN n + 1 > :n THEN 
                    CASE 
                        WHEN :start_n = 1 THEN 1 -- Reset current to Fibonacci start value for n=1
                        WHEN :start_n = 2 THEN 1 -- Reset current to Fibonacci start value for n=2
                        ELSE :a + :b -- Reset to the first calculated Fibonacci value
                    END
                ELSE last_1 + current -- Calculate Fibonacci for the next value in the current iteration
            END AS current
        FROM fib_sequence
        WHERE 
            iteration <= :iteration -- Ensure we do not exceed the iteration limit
        /*+ MATERIALIZE */
    )
    
    SELECT n, current AS value
    FROM fib_sequence
    WHERE n >= :start_n
    and iteration = 1
    ORDER BY iteration,n;
    """)

    # Execute the query with the provided parameters
    results = connection.execute(query, {"a": a, "b": b, "start_n": start_n, "n": n,'iteration':iteration}).fetchall()

    # Fetch and return the results as a list
    fibonacci_numbers = [(row[0], row[1]) for row in results]
    return fibonacci_numbers

def generate_fibonacci_with_sql(connection, start_n, n,iteration=1,intial_sequence=None):
    time_measurement = TimeMeasurement()
    time_measurement.start()
    fib_sequence = __generate_fibonacci_with_sql(connection, start_n, n,iteration,intial_sequence)
    time_measurement.end()
    return time_measurement, fib_sequence