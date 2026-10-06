import React, { useState } from "react";
import "./Register.css";

const Register = () => {
  // 5 campos de estado requeridos por la rúbrica
  const [userName, setUserName] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const gohome = () => {
    window.location.href = window.location.origin;
  };

  const register = async (e) => {
    e.preventDefault();

    let register_url = window.location.origin + "/djangoapp/register";

    try {
      const res = await fetch(register_url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          userName: userName,
          password: password,
          firstName: firstName,
          lastName: lastName,
          email: email,
        }),
      });

      const json = await res.json();
      if (json.status) {
        sessionStorage.setItem("username", json.userName);
        window.location.href = window.location.origin;
      } else if (json.error === "Already Registered") {
        alert("El usuario con este nombre ya se encuentra registrado.");
      } else {
        alert(json.error || "Error al registrar el usuario.");
      }
    } catch (error) {
      console.error("Error en el registro:", error);
      alert("Error al conectar con el servidor.");
    }
  };

  return (
    <div className="register_container">
      <div className="header">
        <span className="text">Sign Up / Registrarse</span>
        <button className="close_btn" onClick={gohome} title="Cerrar">
          &times;
        </button>
      </div>
      <hr />

      <form onSubmit={register}>
        <div className="inputs">
          {/* 1. Nombre de usuario */}
          <div className="input_group">
            <label className="input_label" htmlFor="username">Nombre de usuario (Username)</label>
            <input
              id="username"
              type="text"
              name="username"
              placeholder="Ingresa tu nombre de usuario"
              className="input_field"
              value={userName}
              onChange={(e) => setUserName(e.target.value)}
              required
            />
          </div>

          {/* 2. Nombre */}
          <div className="input_group">
            <label className="input_label" htmlFor="first_name">Nombre (First Name)</label>
            <input
              id="first_name"
              type="text"
              name="first_name"
              placeholder="Ingresa tu primer nombre"
              className="input_field"
              value={firstName}
              onChange={(e) => setFirstName(e.target.value)}
              required
            />
          </div>

          {/* 3. Apellido */}
          <div className="input_group">
            <label className="input_label" htmlFor="last_name">Apellido (Last Name)</label>
            <input
              id="last_name"
              type="text"
              name="last_name"
              placeholder="Ingresa tus apellidos"
              className="input_field"
              value={lastName}
              onChange={(e) => setLastName(e.target.value)}
              required
            />
          </div>

          {/* 4. Correo electrónico */}
          <div className="input_group">
            <label className="input_label" htmlFor="email">Correo Electrónico (Email)</label>
            <input
              id="email"
              type="email"
              name="email"
              placeholder="ejemplo@correo.com"
              className="input_field"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          {/* 5. Contraseña */}
          <div className="input_group">
            <label className="input_label" htmlFor="password">Contraseña (Password)</label>
            <input
              id="password"
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

        {/* Botón de Registro */}
        <div className="submit_panel">
          <button className="submit_btn" type="submit">
            Register / Registrarse
          </button>
        </div>
      </form>
    </div>
  );
};

export default Register;
