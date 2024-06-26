import { useEffect, useState } from "react";
import FileUploader from "../shared/FileUploader/FileUploader";
import Table from "../shared/Table/Table";
import { columnsInitialState } from "./InitialState/UploadFiles.initial";
import UploadFilesService from "./Services/UploadFiles.service";
import { mapApiResponse } from "./Types/UploadFiles.map";
import { AccountData, ApiResponse } from "./Types/UploadFiles.types";

import "./UploadFiles.css";

const UploadFiles = () => {
  const [accountData, setAccountData] = useState<AccountData[]>([]);

  const getAccountsData = async () => {
    const response: ApiResponse[] =
      await UploadFilesService.getTransactionsList();

    const formattedData = mapApiResponse(response);
    setAccountData(formattedData);
  };

  useEffect(() => {
    getAccountsData();
  }, []);

  return (
    <div className="container">
      <div className="section">
        <h1>Subir archivo</h1>
        <FileUploader
          width="100%"
          height="250px"
          maxNumberOfFiles={1}
          filename="account_file"
        />
      </div>
      <div className="section">
        <h1>Contenido de base de datos:</h1>
        <Table columns={columnsInitialState} data={accountData} />
      </div>
    </div>
  );
};
export default UploadFiles;
