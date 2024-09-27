const FetchData = async <T>(url: string): Promise<T> => {
  try {
    const res = await fetch(url);
    if (!res.ok) {
      throw new Error(`HTTP error! Status: ${res.status}`);
    }
    const data: T = await res.json();

    if (data === undefined) {
      throw new Error("Fetched data is undefined.");
    }

    return data;
  } catch (error) {
    console.error("Error fetching data:", error);
    throw error; 
  }
};

export default FetchData;
