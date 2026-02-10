from odoo import models, fields, api
import hashlib
from odoo.exceptions import ValidationError  # Importa per llançar l'error

class MoviesMovie(models.Model):
    _name = 'movies.movie'
    _description = 'Entidad Película'
    _rec_name = 'title'
    title = fields.Char(string='Títol', required=True)
    year = fields.Integer(string='Any d’estrena')
    original_title = fields.Text(string='Títol original')
    synopsis = fields.Text(string='Sinopsi')
    director = fields.Char(string='Director')
    country_id = fields.Char(string='País del ERP')
        
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
   
    

    
    # Campo HASH calculado (Punto 1 del enunciado) 
    hash_code = fields.Char(string='HASH', compute='_compute_hash', store=True)

    # Relación One2many hacia las opiniones [cite: 50]
    view_ids = fields.One2many('movies.view', 'movie_id', string='Visualitzacions/Opinions')

    

 

    @api.depends('title', 'year')
    def _compute_hash(self):
        for record in self:
            if record.title and record.year:
                # Combinamos título y año para el hash 
                raw_data = f"{record.title}{record.year}"
                record.hash_code = hashlib.sha512(raw_data.encode()).hexdigest()
            else:
                record.hash_code = "x"

    @api.depends('view_ids.rating')
    def _compute_average_rating(self):
        for record in self:
            # Obtenemos todas las notas de sus visualizaciones
            ratings = record.view_ids.mapped('rating')
            if ratings:
                record.average_rating = sum(ratings) / len(ratings)
            else:
                record.average_rating = 0.0



    
    
class MoviesView(models.Model):
    _name = 'movies.view'
    _description = 'Entidad Visualització / Opinió'

    # Relación Many2one hacia la película [cite: 52]
    movie_id = fields.Many2one('movies.movie', string='Pel·lícula', ondelete='cascade')
    
    rating = fields.Integer(string='Valoració numèrica')
    review = fields.Text(string='Opinió')
    view_date = fields.Date(string='Dia de visualització')

    owner_dam = fields.Char(
        string='Propietari DAM', 
        readonly=True, 
        default=lambda self: self.env.user.email or self.env.user.name
    )

     # Restricció per a la valoració (Punt 4 de l'enunciat)
    @api.constrains('rating')
    def _check_rating_range(self):
        for record in self:
            if record.rating < 1 or record.rating > 10:
                raise ValidationError("La valoració ha de ser un número entre 1 i 10.")

   