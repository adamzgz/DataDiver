using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
//using DataDiver.Services;


namespace DataDiver.Pages
{
    public class LoginModel : PageModel
    {
        //private readonly AuthService _authService;

        [BindProperty]
        public string CorreoElectronico { get; set; }
        [BindProperty]
        public string Contrasena { get; set; }

        public LoginModel()
        {
            // Aqu� deber�as configurar tu AuthService, posiblemente a trav�s de inyecci�n de dependencias
            /*var dbConnection = new DatabaseConnection("tu_servidor", "tu_base_de_datos", "tu_usuario", "tu_contrase�a");
            _authService = new AuthService(dbConnection);*/
        }

        public void OnGet()
        {
            
        }

        public IActionResult OnPost()
        {
            if (!ModelState.IsValid)
            {
                return Page();
            }

            //var user = _authService.Login(CorreoElectronico, Contrasena);
           /* if (user != null)
            {
                // Implementa la l�gica de sesi�n aqu�
                // Por ejemplo, establecer una cookie de sesi�n o utilizar un mecanismo de autenticaci�n integrado

                return RedirectToPage("/Index"); // Redirige al usuario a la p�gina principal despu�s del login
            }
           */
            ModelState.AddModelError(string.Empty, "Intento de login inv�lido.");
            return Page();
        }
    }
}
