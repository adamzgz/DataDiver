using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using System.Net.Http;
using System.Threading.Tasks;

public class IndexModel : PageModel
{
    private readonly IHttpClientFactory _httpClientFactory;

    public IndexModel(IHttpClientFactory httpClientFactory)
    {
        _httpClientFactory = httpClientFactory;
    }

    [BindProperty]
    public IFormFile UploadedFile { get; set; }

    public void OnGet()
    {
    }

    public async Task<IActionResult> OnPostAsync()
    {
        try
        {
            if (UploadedFile != null && UploadedFile.Length > 0)
            {
                var httpClient = _httpClientFactory.CreateClient();
                var form = new MultipartFormDataContent();

                // Añadir el archivo con su Content-Type
                var streamContent = new StreamContent(UploadedFile.OpenReadStream());
                streamContent.Headers.ContentType = new System.Net.Http.Headers.MediaTypeHeaderValue(UploadedFile.ContentType);
                form.Add(streamContent, "file", UploadedFile.FileName);

                // Añadir el campo overwrite
                form.Add(new StringContent("false"), "overwrite");

                var userId = "1"; // Asegura que el userId sea correcto
                var response = await httpClient.PostAsync($"http://data_loading:8000/upload-dataset/{userId}", form);



                if (response.IsSuccessStatusCode)
                {
                    TempData["Message"] = "Archivo subido con éxito.";
                    return RedirectToPage("/Index");
                }
                else
                {
                    // Para un manejo más detallado de errores, podrías querer leer la respuesta del servidor
                    var errorResponse = await response.Content.ReadAsStringAsync();
                    TempData["ErrorMessage"] = $"No se ha podido subir el archivo. Detalles: {errorResponse}";
                    return RedirectToPage("/Index");
                }
            }
            else
            {
                TempData["ErrorMessage"] = "No se ha seleccionado ningún archivo.";
                return RedirectToPage("/Index");
            }
        }
        catch (Exception e)
        {
            TempData["ErrorMessage"] = $"Ha ocurrido un problema. Detalles: {e.Message}";
            return RedirectToPage("/Index");
        }
    }

}