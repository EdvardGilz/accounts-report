import HTTPWrapper from "../../../services/HTTPWrapper";

class UploadFilesService {
  getTransactionsList = async () => {
    const apiCall = new HTTPWrapper<"accounts">("accounts");
    return await apiCall.addResource("accounts").get();
  };
}

const uploadFilesServiceInstance = new UploadFilesService();

export default uploadFilesServiceInstance;
