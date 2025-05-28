// Funciones para conectarse con el backend
import axios from "axios";

export const getCinemas = async () => {
  const res = await axios.get(`http://localhost:8000/cinemas/`);
  return res.data;
};

export const getShowtimesWithAvailability = async (cinema_id: number) => {
  const res = await axios.get(
    `http://localhost:8000}/showtimes/with-availability/${cinema_id}`
  );
  return res.data;
};

export const getUserInfo = async () => {
  const res = await axios.get(`http://localhost:8000}/users/get/my_info`);
  return res.data;
};

export const createTicketPurchase = async (payload: any) => {
  const res = await axios.post(
    `http://localhost:8000}/tickets/create`,
    payload
  );
  return res.data;
};
