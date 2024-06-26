import { TableColumn } from "react-data-table-component";

export interface TableProps<T> {
  columns: TableColumn<T>[];
  data: T[];
}
