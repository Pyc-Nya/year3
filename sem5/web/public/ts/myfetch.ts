export const HOST = window.location.hostname;
export const host = () => `http://${HOST}:8000`;
export const BASE_IMG_URL = `${host()}/prod-images`;

async function myfetch(path: string, param: RequestInit = {}): Promise<Response> {
  path = host() + "/api" + path;
  // param.credentials = 'include';
  param.headers = {
    "Content-Type": "application/json",
    credentials: "include",
    // "authorization": "Bearer 1",
  };
  // console.log(`fetch to ${path}, method: ${param.method ?? "GET"}`);

  if (navigator.onLine) {
    try {
      const r = await fetch(path, param);
      if (!(200 <= r.status && r.status < 300)) {
        throw new Error(`${r.status}`);
      }
      return r;
    } catch (error) {
      const e = error as Error;
      console.error(`Failed to fetch on ${path}\nresponse status: ${e.message}`);
      throw e; 
    }
  } else {
    const r = await fetch("/offline", param);
    if (!(200 <= r.status && r.status < 300)) {
      throw new Error(`${r.status}`);
    }
    return r;
  }
}

async function makeFetch(url: string, params: RequestInit = {}, onSuccess: Function, onFail: Function) {
  try {
    const r = await myfetch(url, params);
    if (200 <= r.status && r.status < 300) {
      const responseText = await r.text();
      try {
        const d = JSON.parse(responseText);
        onSuccess(d, r);
      } catch (error) {
        onSuccess(responseText);
      }
    } else {
      throw new Error(`${r.status}`);
    }
  } catch (error) {
    onFail();
    const e = error as Error;
    if (e.message !== 'Unexpected end of JSON input') {
      console.error(`Failed to fetch on ${url}\nresponse status: ${e.message}`);
    }
  }
}

export { makeFetch };