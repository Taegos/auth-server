using AuthServer.DTO;
using Microsoft.AspNetCore.Mvc;

using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace AuthServer.Controllers
{

    [ApiController]
    [Route("[controller]")]
    public class AccountController : ControllerBase
    {
        private readonly ILogger<AccountController> _logger;

        public AccountController(ILogger<AccountController> logger)
        {
            _logger = logger;
        }

        [HttpPost]
        public IActionResult Post(JObject payload)
        {
            try
            {
                CreateAccountDTO dto = payload.ToObject<CreateAccountDTO>();           
            } catch (JsonSerializationException e)
            {
                return BadRequest();
            }
            return Ok();
        }
    }
}
