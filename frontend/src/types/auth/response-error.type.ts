export interface ResponseError {
  status: number;
  message: string;
  error: {
    detail: string;
  };
  name: string;
  ok: boolean;
  statusText: string;
  url: string;
}
