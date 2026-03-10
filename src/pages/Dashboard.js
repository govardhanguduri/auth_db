import { useEffect, useState } from "react";
import axios from "axios";
import { Stack, Text, PrimaryButton, Persona, PersonaSize } from "@fluentui/react";

const Dashboard = () => {
  const [user, setUser] = useState({});

  useEffect(() => {
    const fetchUser = async () => {
      const token = localStorage.getItem("token");
      const res = await axios.get("http://localhost:8000/dashboard", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setUser(res.data);
    };
    fetchUser();
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("token");
    window.location.href = "/login";
  };

  return (
    <Stack
      tokens={{ childrenGap: 20 }}
      styles={{ root: { width: 400, margin: "auto", marginTop: 100 } }}
    >
      <Persona
        text={user.username}
        secondaryText={user.email}
        size={PersonaSize.size72}
      />
      <Text variant="large">Welcome back, {user.username}!</Text>
      <PrimaryButton text="Logout" onClick={handleLogout} />
    </Stack>
  );
};

export default Dashboard;