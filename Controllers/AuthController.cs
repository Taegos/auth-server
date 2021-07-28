using Microsoft.AspNetCore.Mvc;

using Microsoft.Extensions.Logging;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace AuthServer.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class AuthenticationController : ControllerBase
    {
        private readonly ILogger<AuthenticationController> _logger;

        public AuthenticationController(ILogger<AuthenticationController> logger)
        {
            _logger = logger;
        }

        [HttpPost]
        public IActionResult Post(JObject payload)
        {

            try
            {
                string email = payload.GetValue("Email").ToString();
                string password = payload.GetValue("Password").ToString();
                string token = AccountRepo.Login(email, password);
                return Ok(token);
            } catch (NullReferenceException e)
            {
                return BadRequest();
            }
            //return Ok(token);
        }
    }
}
