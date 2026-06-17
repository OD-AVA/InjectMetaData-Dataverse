import sys
from schema_builder import SchemaBuilder
from schema_dispatcher import SchemaDispatcher

file_path = sys.argv[1] if len(sys.argv) > 1 else "DictionnaireDeDonnes.xlsx"

builder = SchemaBuilder(file_path)
tables = builder.build()

dispatcher = SchemaDispatcher()
dispatcher.dispatch(tables)

print("[OK] JSON générés")