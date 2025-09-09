var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
export const HOST = window.location.hostname;
export const host = () => `http://${HOST}:8000`;
export const BASE_IMG_URL = `${host()}/prod-images`;
function myfetch(path_1) {
    return __awaiter(this, arguments, void 0, function* (path, param = {}) {
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
                const r = yield fetch(path, param);
                if (!(200 <= r.status && r.status < 300)) {
                    throw new Error(`${r.status}`);
                }
                return r;
            }
            catch (error) {
                const e = error;
                console.error(`Failed to fetch on ${path}\nresponse status: ${e.message}`);
                throw e;
            }
        }
        else {
            const r = yield fetch("/offline", param);
            if (!(200 <= r.status && r.status < 300)) {
                throw new Error(`${r.status}`);
            }
            return r;
        }
    });
}
function makeFetch(url_1) {
    return __awaiter(this, arguments, void 0, function* (url, params = {}, onSuccess, onFail) {
        try {
            const r = yield myfetch(url, params);
            if (200 <= r.status && r.status < 300) {
                const responseText = yield r.text();
                try {
                    const d = JSON.parse(responseText);
                    onSuccess(d, r);
                }
                catch (error) {
                    onSuccess(responseText);
                }
            }
            else {
                throw new Error(`${r.status}`);
            }
        }
        catch (error) {
            onFail();
            const e = error;
            if (e.message !== 'Unexpected end of JSON input') {
                console.error(`Failed to fetch on ${url}\nresponse status: ${e.message}`);
            }
        }
    });
}
export { makeFetch };
