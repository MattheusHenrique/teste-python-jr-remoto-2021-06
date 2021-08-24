import { check, group } from 'k6';
import { Httpx } from 'https://jslib.k6.io/httpx/0.0.3/index.js';

let session = new Httpx({
  baseURL: `http://localhost:8000/api`,
  headers: { 'Content-Type': 'application/json' },
});

const responseToJson = (request) => {
  try {
    return JSON.parse(request.body);
  } catch (error) {
    return {};
  }
};

const shallowObjectCompare = (expected, received) => {
  return Object.keys(expected).every(k => expected[k] === received[k]);
}

export default () => {

  group("Cria projeto magpy", () => {
    session.delete("/projects/magpy/");  // <- limpa o ambiente antes do teste

    const magpyData = {
        name: "magpy",
        packages: [
            {name: "Django"}
        ]
    };
    const magpy = session.post("/projects/", JSON.stringify(magpyData));

    check(magpy, {
      "Cria o projeto com sucesso": (r) => r.status === 201,
    });

    check(magpy, {
      "O pacote Django esta na versão mais recente": (r) => {
        const data = responseToJson(r);
        const django = data.packages.find((p) => p.name === "Django");
        return django.version === "3.2.6";
      },
    });
  });


   group("Cria projeto com pacote vazio", () => {
    session.delete("/projects/empty/");  // <- limpa o ambiente antes do teste

    const emptyData = {
        name: "empty",
        packages: []
    };
    const empty = session.post("/projects/", JSON.stringify(emptyData));

    check(empty, {
      "Tentativa resulta em erro BAD REQUEST": (r) => r.status === 400,
    });

    check(empty, {
      "Apresenta mensagem de erro": (r) => {
        const data = responseToJson(r);
        const expected = {"error": "At least one package must exist"};
        return shallowObjectCompare(expected, data);
      },
    });
  });


  group("Cria projeto magpy", () => {
    session.delete("/projects/magpy/");  // <- limpa o ambiente antes do teste

    const magpyData = {
        name: "magpy",
        packages: [
            {name: "Django"}
        ]
    };
    const magpy = session.post("/projects/", JSON.stringify(magpyData));

    check(magpy, {
      "Cria o projeto com sucesso": (r) => r.status === 201,
    });

    check(magpy, {
      "O pacote Django esta na versão mais recente": (r) => {
        const data = responseToJson(r);
        const django = data.packages.find((p) => p.name === "Django");
        return django.version === "3.2.6";
      },
    });
  });


  group("Envia projeto com dados invalidos", () => {
    session.delete("/projects/machine-head/");  // <- limpa o ambiente antes do teste

    const mhdData = {
        name: "machine-head",
    };
    const mh = session.post("/projects/", JSON.stringify(mhdData));

    check(mh, {
      "Tentativa resulta em erro BAD REQUEST": (r) => r.status === 400,
    });
  });



  group("Envia projeto com nome de pacote invalido, sem versão", () => {
    session.delete("/projects/titan/");  // <- limpa o ambiente antes do teste

    const titanData = {
      name: "titan",
      packages: [
        {name: 'djangor'}
      ]
    };
    const titan = session.post("/projects/", JSON.stringify(titanData));

    check(titan, {
      "Tentativa resulta em erro BAD REQUEST": (r) => r.status === 400,
    });

    check(titan, {
      "Apresenta mensagem de erro": (r) => {
        const data = responseToJson(r);
        const expected = {"error": "One or more packages doesn't exist"};
        return shallowObjectCompare(expected, data);
      },
    });
  });


    group("Envia projeto com nome de pacote invalido, sem versão", () => {
    session.delete("/projects/titan/");  // <- limpa o ambiente antes do teste

    const titanData = {
      name: "titan",
      packages: [
        {name: 'djangor'}
      ]
    };
    const titan = session.post("/projects/", JSON.stringify(titanData));

    check(titan, {
      "Tentativa resulta em erro BAD REQUEST": (r) => r.status === 400,
    });

    check(titan, {
      "Apresenta mensagem de erro": (r) => {
        const data = responseToJson(r);
        const expected = {"error": "One or more packages doesn't exist"};
        return shallowObjectCompare(expected, data);
      },
    });
  });


  group("Envia projeto com versão invalida", () => {
    session.delete("/projects/titan1/");  // <- limpa o ambiente antes do teste

    const titan1Data = {
      name: "titan1",
      packages: [
        {name: 'django', version: '9.0'}
      ]
    };
    const titan1 = session.post("/projects/", JSON.stringify(titan1Data));

    check(titan1, {
      "Tentativa resulta em erro BAD REQUEST": (r) => r.status === 400,
    });

    check(titan1, {
      "Apresenta mensagem de erro": (r) => {
        const data = responseToJson(r);
        const expected = {"error": "One or more packages doesn't exist"};
        return shallowObjectCompare(expected, data);
      },
    });
  });

};
