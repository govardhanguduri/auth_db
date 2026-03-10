import { useState } from "react";
import { login } from "../api";
import { useNavigate } from "react-router-dom";
import {
  PrimaryButton,
  TextField,
  Stack,
  MessageBar,
  MessageBarType,
  Text,
} from "@fluentui/react";

const Login = () => {
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleChange = (e, newValue) =>
    setForm({ ...form, [e.target.name]: newValue });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      const res = await login(form);
      localStorage.setItem("token", res.data.access_token);
      navigate("/dashboard");
    } catch (err) {
      setError(err.response?.data?.detail || "Login failed");
      alert("Incorrect credentials. Please signup if new.");
      navigate("/signup");
    }
  };

  return (
    <Stack
      horizontalAlign="center"
      verticalAlign="center"
      styles={{
        root: {
          height: "100vh",
          backgroundColor: "#f3f2f1",
          padding: 20,
        },
      }}
    >
      <Stack
        tokens={{ childrenGap: 15 }}
        styles={{
          root: {
            backgroundColor: "white",
            padding: 30,
            width: 320,
            boxShadow: "0 4px 12px rgba(0,0,0,0.15)",
            borderRadius: 8,
          },
        }}
      >
        <Text variant="xLarge" block styles={{ root: { fontWeight: 600, marginBottom: 8 } }}>
          Login Form
        </Text>
        <Text variant="small" styles={{ root: { color: "#666", marginBottom: 20 } }}>
          Enter your credentials to continue
        </Text>

        {error && (
          <MessageBar messageBarType={MessageBarType.error}>{error}</MessageBar>
        )}

        <TextField
          label="Email"
          name="email"
          type="email"
          value={form.email}
          onChange={handleChange}
          required
          styles={{ root: { width: "100%" } }}
          placeholder="Email"
        />
        <TextField
          label="Password"
          name="password"
          type="password"
          canRevealPassword
          value={form.password}
          onChange={handleChange}
          required
          styles={{ root: { width: "100%" } }}
          placeholder="Password"
        />
        <PrimaryButton
          text="Login"
          onClick={handleSubmit}
          styles={{ root: { marginTop: 10 } }}
        />

        <Stack horizontal horizontalAlign="center">
          <Text variant="small" styles={{ root: { color: "#666" } }}>
            Don&apos;t have an account?{" "}
          </Text>
          <Text
            variant="small"
            styles={{ root: { cursor: "pointer", color: "#0078d4", marginLeft: 5 } }}
            onClick={() => navigate("/signup")}
          >
            Sign Up
          </Text>
        </Stack>
      </Stack>
    </Stack>
  );
};

export default Login;