import axios from "axios";

const BASE_URL = "http://127.0.0.1:8000";

export const getData = async () => {
  const response = await axios.get(`${BASE_URL}/data/`);
  return response.data;
};

export const getPrediction = async (kecamatan, steps) => {
  const response = await axios.get(`${BASE_URL}/predict/`, {
    params: { kecamatan, steps },
  });
  return response.data;
};
