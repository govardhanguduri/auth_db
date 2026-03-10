/* eslint-disable jsx-a11y/anchor-is-valid */
import { useState } from "react";
import { signup } from "../api";
import { useNavigate } from "react-router-dom";
import {
  PrimaryButton,
  TextField,
  Stack,
  MessageBar,
  MessageBarType,
  Text,
} from "@fluentui/react";

const Signup = () => {
  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
  });
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleChange = (e, newValue) =>
    setForm({ ...form, [e.target.name]: newValue });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (form.password !== form.confirmPassword) {
      return setError("Passwords do not match");
    }

    try {
      await signup({
        username: form.username,
        email: form.email,
        password: form.password,
      });
      alert("Signup successful! Please login.");
      navigate("/login");
    } catch (err) {
      setError(err.response?.data?.detail || "Signup failed");
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
          Create Account
        </Text>
        <Text variant="small" styles={{ root: { color: "#666", marginBottom: 20 } }}>
          Please fill in the form to create an account
        </Text>

        {error && (
          <MessageBar messageBarType={MessageBarType.error}>{error}</MessageBar>
        )}

        <TextField
          label="Username"
          name="username"
          value={form.username}
          onChange={handleChange}
          required
          styles={{ root: { width: "100%" } }}
          placeholder="Username"
        />
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
        <TextField
          label="Confirm Password"
          name="confirmPassword"
          type="password"
          canRevealPassword
          value={form.confirmPassword}
          onChange={handleChange}
          required
          styles={{ root: { width: "100%" } }}
          placeholder="Confirm Password"
        />
        <PrimaryButton
          text="Sign Up"
          onClick={handleSubmit}
          styles={{ root: { marginTop: 10 } }}
        />
        <Text
          variant="small"
          styles={{ root: { textAlign: "center", marginTop: 15, color: "#666" } }}
        >
          Already have an account?{" "}
          <a href="#" onClick={() => navigate("/login")} style={{ color: "#0078d4", cursor: "pointer" }}>
            Login
          </a>
        </Text>
      </Stack>
    </Stack>
  );
};

export default Signup;