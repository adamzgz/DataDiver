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
                var streamContent = new StreamContent(UploadedFile.OpenReadStream());
                form.Add(streamContent, "file", UploadedFile.FileName);
                form.Add(new StringContent("False"), "overwrite");

                var userId = "1"; // AQUI EL ID DE USUARIO
                var response = await httpClient.PostAsync($"http://data_loading:8000/upload-dataset/{userId}", form);

                if (response.IsSuccessStatusCode)
                {
                    TempData["Message"] = "Archivo subido con éxito.";
                    return RedirectToPage("/Index");
                }
                else
                {
                    TempData["ErrorMessage"] = "No se ha podido subir el archivo.";
                    return RedirectToPage("/Index");
                }
            }
            else
            {
                TempData["ErrorMessage"] = "No se ha seleccionado ningún archivo.";
            }
        }
        catch (Exception e)
        {
            TempData["ErrorMessage"] = "Ha ocurrido un problema.";
            return RedirectToPage("/Index");
        }

        return RedirectToPage("/Index");
    }
}
