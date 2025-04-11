const BASE_URL = import.meta.env.VITE_API_URL;

export const request = async ({
  endpoint,
  method = "GET" | "POST" | "PUT" | "DELETE",
  body,
  onSuccess,
  onFailure,
}) => {
  try {
    const response = await fetch(`${BASE_URL}${endpoint}`, {
      method,
      headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
          "Content-Type": "application/json",
      },
      body,
    });

    if (!response.ok) {
      const { message } = await response.json();
      throw new Error(message);
    }
    const data = await response.json();
    onSuccess(data);
    
  } catch (error) {
    if (error instanceof Error) {
      onFailure(error.message);
    } else {
      onFailure("An error occurred. Please try again later.");
    }
  }
};