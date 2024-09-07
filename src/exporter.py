import os
import pandas as pd


class DataExporter:
    def export_to_csv(self, data, file_path, raise_exception=False):
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            df = pd.DataFrame(data)
            df.to_csv(file_path, index=False, encoding='utf-8')
            print(f"Data successfully exported to {file_path}")
        except Exception as e:
            print(f"Error exporting data: {e}")
            if raise_exception:
                raise e
