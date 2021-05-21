import axios from "axios";
import { settings } from "@/settings";

const API_SERVER = settings.API_SERVER;

export const api_routes = {
  user: {
    login: API_SERVER + "auth/login",
    signup: API_SERVER + "auth/signup",
    profile: API_SERVER + "profile",
    instances: API_SERVER + "instances",
    apply: API_SERVER + "apply",
    applied: API_SERVER + "applied",
    release: API_SERVER + "release",
  }
};

export const apiCall = ({ url, method, ...args }) =>
  new Promise((resolve, reject) => {
    let token = localStorage.getItem("user-token") || " ";
    console.log("token", token);
    if (token)
      axios.defaults.headers.common["Authorization"] = token;

    try {
      console.log("api call", url);
      axios({
        method: method || "get",
        url: url,
        ...args
      })
      .then(resp => {
        resolve(resp.data);
      })
      .catch(error => {
        reject(error);
      });
    } catch (err) {
      reject(new Error(err));
    }
  });
