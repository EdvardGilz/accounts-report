import { AccountData, ApiResponse } from "./UploadFiles.types";

export const mapApiResponse = (apiResponse: ApiResponse[]): AccountData[] => {
  return apiResponse.map((item) => ({
    id: item.id,
    date: item.date,
    accountId: item.account_id,
    transaction: item.transaction,
  }));
};
