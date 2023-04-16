from sqlalchemy import Table

CREATE_VERSION_TRIGGER_KEY = 'CREATE_VERSION_TRIGGER_KEY'
DELETE_VERSION_TRIGGER_KEY = 'DELETE_VERSION_TRIGGER_KEY'


def declare_version_table(table: Table, version_table_name: str):
    """
    Declare new table for store historical data of original table
    :param table: Original table
    :param version_table_name: Name for new table
    :return: Table with same columns as `table` plus `version` integer column
    """

    def _col_copy(col):
        col = col.copy()
        col.unique = False
        col.default = col.server_default = None
        col.autoincrement = False
        col.nullable = True
        col._user_defined_nullable = col.nullable
        col.primary_key = False
        return col

    return Table(
        version_table_name,
        table.metadata,
        *[_col_copy(x) for x in table.columns],
        info={
            CREATE_VERSION_TRIGGER_KEY: get_create_version_trigger_sql(
                schema=table.schema, table_name=table.name, version_table_name=version_table_name
            ),
            DELETE_VERSION_TRIGGER_KEY: get_delete_version_trigger_sql(
                schema=table.schema, table_name=table.name
            ),
        }
    )


def generate_trigger_name(table_name: str) -> tuple:
    trigger_name = f'tg_{table_name}_versions'
    function_name = f'process_{trigger_name}'
    return trigger_name, function_name


def get_create_version_trigger_sql(schema: str, table_name: str, version_table_name: str):
    trigger_name, function_name = generate_trigger_name(table_name)
    return f"""
       create or replace function {function_name}()
       returns trigger as ${trigger_name}$
       declare
       main_table_columns text;

       begin
           select  string_agg(column_name, ',')
           into    main_table_columns
           from information_schema.columns
           where table_schema = '{schema}'
             and table_name   = '{table_name}';

           execute format(
               'insert into {schema}.{version_table_name} ( %s ) VALUES ($1.*) ',
                main_table_columns
           ) using OLD;

           RETURN NEW;
       end;
       ${trigger_name}$ language plpgsql;


       create trigger {trigger_name}
       after update on {schema}.{table_name}
       for each row execute procedure {function_name}();    
    """


def get_delete_version_trigger_sql(schema: str, table_name: str):
    trigger_name, function_name = generate_trigger_name(table_name)
    return (f"drop function {function_name}() cascade; "
            f"drop trigger if exists  {trigger_name} on {schema}.{table_name};")
