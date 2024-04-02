using System;

using System.Security.Cryptography;

namespace DataDiver.Models
{
    public class Usuario
    {
        public int Id { get; set; } // Identificador �nico para el usuario
        public string CorreoElectronico { get; set; } // Correo electr�nico del usuario
        public string Contrasena { get; set; } // Hash de la contrase�a del usuario

        // El tama�o del salt y del hash son espec�ficos del algoritmo utilizado.
        private const int SaltSize = 16;
        private const int HashSize = 20;
        private const int Iterations = 10000; // N�mero de iteraciones.

        // Almacena el hash de la contrase�a internamente
        private string contrasenaHash;

        public Usuario(int id, string correoElectronico, string contrasenaHash)
        {
            Id = id;
            CorreoElectronico = correoElectronico;
            Contrasena = contrasenaHash;
        }
        public Usuario(string correoElectronico, string contrasenaHash)
        {
            CorreoElectronico = correoElectronico;
            Contrasena = contrasenaHash;
        }
        public Usuario()
        {

        }

        // Propiedad p�blica para acceder al hash de la contrase�a de forma segura.
        public string ContrasenaHash
        {
            get { return contrasenaHash; }
            private set { contrasenaHash = value; }
        }

        // M�todo para hashear y establecer la contrase�a.
        public void SetPassword(string password)
        {
            using (var rng = new RNGCryptoServiceProvider())
            {
                byte[] salt = new byte[SaltSize];
                rng.GetBytes(salt);

                using (var pbkdf2 = new Rfc2898DeriveBytes(password, salt, Iterations))
                {
                    byte[] hash = pbkdf2.GetBytes(HashSize);

                    byte[] hashBytes = new byte[SaltSize + HashSize];
                    Array.Copy(salt, 0, hashBytes, 0, SaltSize);
                    Array.Copy(hash, 0, hashBytes, SaltSize, HashSize);

                    ContrasenaHash = Convert.ToBase64String(hashBytes);
                }
            }
        }

        // M�todo para verificar si una contrase�a coincide con el hash almacenado.
        public bool VerifyPassword(string password)
        {
            byte[] hashBytes = Convert.FromBase64String(ContrasenaHash);
            byte[] salt = new byte[SaltSize];
            Array.Copy(hashBytes, 0, salt, 0, SaltSize);

            using (var pbkdf2 = new Rfc2898DeriveBytes(password, salt, Iterations))
            {
                byte[] hash = pbkdf2.GetBytes(HashSize);
                for (int i = 0; i < HashSize; i++)
                {
                    if (hashBytes[i + SaltSize] != hash[i])
                    {
                        return false;
                    }
                }
                return true;
            }
        }
    }
}
