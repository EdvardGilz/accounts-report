import DataTable from "react-data-table-component";
import { TableProps } from "./Table.types";

const Table = <T,>(props: TableProps<T>) => {
  const { columns, data } = props;
  return <DataTable columns={columns} data={data} />;
};
export default Table;
