from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from .models import Usuario, Terreno, Vivienda, Residente


class SmartConnectTests(APITestCase):

    def setUp(self):
        User = get_user_model()

        self.admin = User.objects.create_user(
            "admin_demo",
            password="ClaveDemo123!",
            is_staff=True
        )

        self.owner = User.objects.create_user(
            "owner_demo",
            password="ClaveDemo123!"
        )

        self.tenant = User.objects.create_user(
            "tenant_demo",
            password="ClaveDemo123!"
        )

        self.p = Usuario.objects.create(
            cuenta=self.owner,
            rut="10000000-8",
            nombre="Ana",
            apellido="Demo",
            telefono="123",
            correo="ana@example.com"
        )

        self.q = Usuario.objects.create(
            cuenta=self.tenant,
            rut="20000000-1",
            nombre="Luis",
            apellido="Demo",
            telefono="456",
            correo="luis@example.com"
        )

        self.a = Terreno.objects.create(
            nombre="A",
            direccion="Demo A"
        )

        self.b = Terreno.objects.create(
            nombre="B",
            direccion="Demo B"
        )

        self.a.administradores.add(self.p)

        self.v = Vivienda.objects.create(
            terreno=self.a,
            numero=1
        )

        self.w = Vivienda.objects.create(
            terreno=self.b,
            numero=1
        )

    def test_jwt(self):
        self.assertEqual(
            self.client.get("/api/terrenos/").status_code,
            401
        )

        r = self.client.post(
            "/api/token/",
            {
                "username": "owner_demo",
                "password": "ClaveDemo123!"
            },
            format="json"
        )

        self.assertEqual(r.status_code, 200)

        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + r.data["access"]
        )

        self.assertEqual(
            self.client.get("/api/terrenos/").status_code,
            200
        )

        self.assertEqual(
            self.client.post(
                "/api/token/refresh/",
                {"refresh": r.data["refresh"]},
                format="json"
            ).status_code,
            200
        )

    def test_asignacion(self):
        self.client.force_authenticate(self.owner)

        data = {
            "usuario": self.q.pk,
            "vivienda": self.v.pk,
            "rol_residente": "ARRENDATARIO"
        }

        self.assertEqual(
            self.client.post(
                "/api/residentes/",
                data,
                format="json"
            ).status_code,
            201
        )

        self.assertEqual(
            self.client.post(
                "/api/residentes/",
                data,
                format="json"
            ).status_code,
            400
        )

        self.assertEqual(
            self.client.post(
                "/api/residentes/",
                dict(data, vivienda=self.w.pk),
                format="json"
            ).status_code,
            403
        )

        self.assertEqual(
            self.client.post(
                "/api/residentes/",
                dict(data, rol_residente="PROPIETARIO_ADMIN"),
                format="json"
            ).status_code,
            403
        )

        self.assertEqual(Residente.objects.count(), 1)

        self.client.force_authenticate(self.tenant)

        self.assertEqual(
            self.client.post(
                "/api/residentes/",
                data,
                format="json"
            ).status_code,
            403
        )

        self.assertEqual(
            self.client.get(
                f"/api/viviendas/{self.w.pk}/"
            ).status_code,
            403
        )

        self.assertEqual(Residente.objects.count(), 1)

    def test_crud(self):
        self.client.force_authenticate(self.admin)

        for ruta, datos in [
            (
                "usuarios",
                {
                    "rut": "12345678-5",
                    "nombre": "Eva",
                    "apellido": "Demo",
                    "telefono": "123",
                    "correo": "eva@example.com"
                }
            ),
            (
                "terrenos",
                {
                    "nombre": "C",
                    "direccion": "Demo C"
                }
            ),
            (
                "viviendas",
                {
                    "terreno": self.a.pk,
                    "numero": 99
                }
            ),
            (
                "puntos-acceso",
                {
                    "terreno": self.a.pk,
                    "nombre": "Entrada",
                    "hora_desde": "08:00",
                    "hora_hasta": "22:00"
                }
            ),
        ]:

            url = f"/api/{ruta}/"

            r = self.client.post(
                url,
                datos,
                format="json"
            )

            self.assertEqual(r.status_code, 201, r.data)

            detalle = f'{url}{r.data["id"]}/'

            self.assertEqual(
                self.client.get(url).status_code,
                200
            )

            self.assertEqual(
                self.client.get(detalle).status_code,
                200
            )

            self.assertEqual(
                self.client.put(
                    detalle,
                    datos,
                    format="json"
                ).status_code,
                200
            )

            self.assertEqual(
                self.client.delete(detalle).status_code,
                204
            )

        self.assertEqual(
            self.client.delete(
                f"/api/terrenos/{self.a.pk}/"
            ).status_code,
            400
        )