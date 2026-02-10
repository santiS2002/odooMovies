from odoo import models, fields, api
import hashlib
import requests  # Importante para la llamada a la API
from odoo.exceptions import ValidationError

class MoviesMovie(models.Model):
    _name = 'movies.movie'
    _description = 'Entidad Película'
    _rec_name = 'title'

    title = fields.Char(string='Títol', required=True)
    year = fields.Integer(string='Any d’estrena')
    original_title = fields.Text(string='Títol original')
    synopsis = fields.Text(string='Sinopsi')
    director = fields.Char(string='Director')
    
    # Cambio de Char a Many2one para usar el modelo res.country 
    country_id = fields.Many2one('res.country', string='País base') 
    
    #  Campos de recaudación en dólares y euros [cite: 32, 45, 46]
    recaptacio_dolars = fields.Float(string='Recaptació en Dòlars')
    recaptacio_euros = fields.Float(
        string='Recaptació en Euros', 
        compute='_compute_recaptacio_euros', 
        store=True
    )

    platform = fields.Selection(
        selection=[
            ('netflix', 'Netflix'),
            ('prime', 'Amazon Prime Video'),
            ('disney', 'Disney+'),
            ('hbo', 'HBO Max'),
            ('cinema', 'Cinema'),
            ('altres', 'Altres')
        ],
        string='Plataforma',
        default='cinema',
        help="Plataforma on s'ha vist la pel·lícula"
    )
    
    theme = fields.Selection(
        selection=[
            ('drama', 'Drama'),
            ('terror', 'Terror'),
            ('comedia', 'Comèdia'),
            ('accio', 'Acció'),
            ('ciencia_ficcio', 'Ciència-Ficció'),
            ('altres', 'Altres')
        ],
        string='Temàtica',
        default='drama'
    )
    
    average_rating = fields.Float(
        string='Valoració Mitjana', 
        compute='_compute_average_rating', 
        store=True,
        readonly=True
    )

    hash_code = fields.Char(string='HASH', compute='_compute_hash', store=True)
    view_ids = fields.One2many('movies.view', 'movie_id', string='Visualitzacions/Opinions')

    # Lógica para calcular la conversión de moneda 
    @api.depends('recaptacio_dolars')
    def _compute_recaptacio_euros(self):
        # Usamos una API pública de tipos de cambio
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        try:
            response = requests.get(url)
            data = response.json()
            rate = data.get('rates', {}).get('EUR', 0.92) # 0.92 como fallback si falla
        except Exception:
            rate = 0.92 # Valor aproximado si no hay internet

        for record in self:
            record.recaptacio_euros = record.recaptacio_dolars * rate

    @api.depends('title', 'year')
    def _compute_hash(self):
        for record in self:
            if record.title and record.year:
                raw_data = f"{record.title}{record.year}"
                record.hash_code = hashlib.sha512(raw_data.encode()).hexdigest()
            else:
                record.hash_code = "x"

    @api.depends('view_ids.rating')
    def _compute_average_rating(self):
        for record in self:
            ratings = record.view_ids.mapped('rating')
            if ratings:
                record.average_rating = sum(ratings) / len(ratings)
            else:
                record.average_rating = 0.0

class MoviesView(models.Model):
    _name = 'movies.view'
    _description = 'Entidad Visualització / Opinió'

    movie_id = fields.Many2one('movies.movie', string='Pel·lícula', ondelete='cascade')
    rating = fields.Integer(string='Valoració numèrica')
    review = fields.Text(string='Opinió')
    view_date = fields.Date(string='Dia de visualització')

    owner_dam = fields.Char(
        string='Propietari DAM', 
        readonly=True, 
        default=lambda self: self.env.user.email or self.env.user.name
    )

    @api.constrains('rating')
    def _check_rating_range(self):
        for record in self:
            if record.rating < 1 or record.rating > 10:
                raise ValidationError("La valoració ha de ser un número entre 1 i 10.")