export type API = "accounts";

export interface APIAttributes {
  accounts: {};
}

export interface SegmentTypes {
  accounts: "accounts";
}

export const endpointsList = {
  accounts: `${process.env.REACT_APP_API_ENDPOINT}/${process.env.REACT_APP_ENV}`,
};
