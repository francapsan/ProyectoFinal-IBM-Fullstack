import React, { useState } from "react";
import "./Login.css";

const Login = ({ onClose }) => {
  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");

  const login = async (e) => {
    e.preventDefault();
    let login_url = window.location.origin + "/djangoapp/login";

    try {
      const res = await fetch(login_url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          userName: userName,
          password: password,
        }),
      });

      const json = await res.json();
      if (json.status === "Authenticated") {
        sessionStorage.setItem("username", json.userName);
        window.location.href = window.location.origin;
      } else {
        alert("Usuario o contraseña incorrectos.");
      }
    } catch (err) {
      console.error("Error en login:", err);
      alert("Error al conectar con el servidor.");
    }
  };

  return (
    <div className="login_container">
      <div className="header">
        <span className="text">Login / Iniciar Sesión</span>
        <button className="close_btn" onClick={() => window.location.href = window.location.origin}>
          &times;
        </button>
      </div>
      <hr />
      <form onSubmit={login}>
        <div className="inputs">
          <div className="input_group">
            <label className="input_label">Nombre de Usuario</label>
            <input
              type="text"
              name="username"
              placeholder="Username"
              className="input_field"
              value={userName}
              onChange={(e) => setUserName(e.target.value)}
              required
            />
          </div>
          <div className="input_group">
            <label className="input_label">Contraseña</label>
            <input
              type="password"
              name="password"
              placeholder="••••••••"
              className="input_field"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
        </div>
        <div className="submit_panel">
          <button className="submit_btn" type="submit">Login</button>
        </div>
      </form>
    </div>
  );
};

export default Login;
