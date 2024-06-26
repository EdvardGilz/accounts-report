import { buildUrl } from "build-url-ts";

import {
  API,
  APIAttributes,
  SegmentTypes,
  endpointsList,
} from "./HTTPWrapper.types";

type EndpointKey = keyof typeof endpointsList;

interface FetchOptions {
  headers?: Record<string, string>;
  method?: string;
  body?: Record<string, any>;
}

class HTTPWrapper<T extends API> {
  private baseURL: string;
  private segments: string[] = [];
  private queryParameters: Partial<APIAttributes[T]> = {};

  constructor(baseURL: EndpointKey) {
    this.baseURL = endpointsList[baseURL] ?? "";
  }

  async get(): Promise<null | any> {
    return this.fetch({ method: "GET" });
  }
  async post(body?: Record<string, any>): Promise<null | any> {
    return this.fetch({ method: "POST", body });
  }

  addResource(resource: SegmentTypes[T], id?: number): this {
    this.segments.push(resource);
    if (id !== undefined) {
      this.segments.push(id.toString());
    }
    return this;
  }

  addQueryParam<K extends keyof APIAttributes[T]>(
    key: K,
    value: APIAttributes[T][K]
  ): this {
    this.queryParameters[key] = value;
    return this;
  }

  private buildCustomURL(): string {
    const queryParameters: any = this.queryParameters;
    const url = buildUrl(this.baseURL, {
      path: this.segments.join("/"),
      queryParams: queryParameters,
    });
    return url ?? "";
  }

  private async fetch(options: FetchOptions = {}): Promise<null | any> {
    try {
      const { body } = options;
      const headers: Record<string, string> = {
        "Content-Type": "application/json",
      };

      const response = await fetch(this.buildCustomURL(), {
        body: body ? JSON.stringify(body) : null,
        headers,
      });

      const result = await response?.json();

      if ("error" in result) {
        alert("Ha ocurrido un error al procesar la solicitud 1");
        return null;
      }
      return result;
    } catch (error) {
      alert("Ha ocurrido un error al procesar la solicitud 2");
      return null;
    }
  }
}

export default HTTPWrapper;
