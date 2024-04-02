/*using DataDiver.DAL; // Asegúrate de que este namespace sea correcto para DatabaseConnection
using DataDiver.Models; // Asegúrate de que este namespace sea correcto para Usuario
using System; // Para Convert.ToInt32, Convert.ToString
using DataDiver.Services;


namespace DataDiver.Services
{
    public class AuthService
    {
        private readonly DatabaseConnection _dbConnection;

        public AuthService(DatabaseConnection dbConnection)
        {
            _dbConnection = dbConnection;
        }

        public bool RegisterUser(string correoElectronico, string contrasena)
        {
            var usuario = new Usuario(correoElectronico, contrasena);
            usuario.SetPassword(contrasena);

            var query = $"INSERT INTO Usuarios (CorreoElectronico, Contrasena) VALUES ('{correoElectronico}', '{usuario.ContrasenaHash}')";
            try
            {
                _dbConnection.ExecuteNonQuery(query);
                return true;
            }
            catch
            {
                // Este bloque catch está capturando todas las excepciones. Considera capturar y manejar excepciones específicas.
                return false;
            }
        }

        public Usuario Login(string correoElectronico, string contrasena)
        {
            var query = $"SELECT Id, CorreoElectronico, Contrasena FROM Usuarios WHERE CorreoElectronico = '{correoElectronico}'";
            var dataTable = _dbConnection.ExecuteQuery(query);

            if (dataTable.Rows.Count == 1)
            {
                var row = dataTable.Rows[0];
                var usuario = new Usuario
                {
                    Id = Convert.ToInt32(row["Id"]),
                    CorreoElectronico = Convert.ToString(row["CorreoElectronico"]),
                    Contrasena = Convert.ToString(row["Contrasena"]) // Asume que esto es el hash de la contraseña
                };

                if (usuario.VerifyPassword(contrasena))
                {
                    return usuario;
                }
            }

            return null;
        }
    }
}*/
