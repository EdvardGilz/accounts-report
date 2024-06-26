import { TableColumn } from "react-data-table-component";
import { AccountData } from "../Types/UploadFiles.types";

export const columnsInitialState: TableColumn<AccountData>[] = [
  {
    name: "ID",
    selector: (row: AccountData) => row.id,
    sortable: true,
  },
  {
    name: "Date",
    selector: (row: AccountData) => row.date,
    sortable: true,
  },
  {
    name: "Account ID",
    selector: (row: AccountData) => row.accountId.toString(),
  },
  {
    name: "Transaction",
    selector: (row: AccountData) => row.transaction.toString(),
  },
];
