import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime


class NessusAnalyzer:
    def __init__(self, csv_path):
        """
        Initialize the NessusAnalyzer with the path to the CSV file

        Args:
            csv_path (str): Path to the Nessus CSV export file
        """
        self.csv_path = csv_path
        self.df = None
        self.load_data()

    def load_data(self):
        """Load and perform initial cleaning of the Nessus CSV data"""
        try:
            self.df = pd.read_csv(self.csv_path, low_memory=False)
            print(f"Datos cargados exitosamente. Dimensiones: {self.df.shape}")
        except Exception as e:
            print(f"Error al cargar el archivo: {str(e)}")
            return

        # Convertir nombres de columnas a un formato más manejable
        self.df.columns = self.df.columns.str.strip().str.lower().str.replace(' ', '_')

    def clean_data(self):
        """Limpieza básica de datos"""
        if self.df is None:
            return

        # Eliminar duplicados
        self.df.drop_duplicates(inplace=True)

        # Rellenar valores nulos
        self.df.fillna({'risk': 'No definido', 'description': 'Sin descripción'}, inplace=True)

        # Normalizar niveles de riesgo
        risk_mapping = {
            'Critical': 'Critical',
            'High': 'High',
            'Medium': 'Medium',
            'Low': 'Low',
            'None': 'Info',
            'Info': 'Info'
        }
        self.df['risk'] = self.df['risk'].map(risk_mapping).fillna('Info')

    def analyze_vulnerabilities(self):
        """
        Realizar análisis básico de vulnerabilidades

        Returns:
            dict: Diccionario con estadísticas del análisis
        """
        if self.df is None:
            return {}

        analysis = {
            'total_vulnerabilities': len(self.df),
            'by_risk_level': self.df['risk'].value_counts().to_dict(),
            'unique_hosts': self.df['host'].nunique(),
            'critical_hosts': self.df[self.df['risk'] == 'Critical']['host'].nunique()
        }

        return analysis

    def get_critical_vulnerabilities(self):
        """
        Obtener todas las vulnerabilidades críticas

        Returns:
            pandas.DataFrame: DataFrame con vulnerabilidades críticas
        """
        if self.df is None:
            return pd.DataFrame()

        return self.df[self.df['risk'] == 'Critical'].sort_values('host')

    def plot_risk_distribution(self, save_path=None):
        """
        Crear gráfico de distribución de riesgos

        Args:
            save_path (str, optional): Ruta donde guardar el gráfico. Si es None, se muestra en pantalla.
        """
        if self.df is None:
            return

        plt.figure(figsize=(10, 6))
        sns.countplot(data=self.df, x='risk', order=['Critical', 'High', 'Medium', 'Low', 'Info'])
        plt.title('Distribución de Vulnerabilidades por Nivel de Riesgo')
        plt.xlabel('Nivel de Riesgo')
        plt.ylabel('Cantidad')
        plt.xticks(rotation=45)

        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
            plt.close()
        else:
            plt.show()

    def export_results(self, output_dir):
        """
        Exportar resultados del análisis

        Args:
            output_dir (str): Directorio donde guardar los archivos de resultados
        """
        if self.df is None:
            return

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Exportar vulnerabilidades críticas
        critical_vulns = self.get_critical_vulnerabilities()
        critical_vulns.to_csv(f'{output_dir}/vulnerabilidades_criticas_{timestamp}.csv', index=False)

        # Exportar resumen general
        summary = pd.DataFrame([self.analyze_vulnerabilities()])
        summary.to_csv(f'{output_dir}/resumen_analisis_{timestamp}.csv', index=False)

        # Generar y guardar gráfico
        self.plot_risk_distribution(f'{output_dir}/distribucion_riesgos_{timestamp}.png')


def main():
    """Función principal de ejemplo"""
    # Crear instancia del analizador
    analyzer = NessusAnalyzer('resultados_nessus.csv')

    # Limpiar datos
    analyzer.clean_data()

    # Realizar análisis
    analysis_results = analyzer.analyze_vulnerabilities()
    print("\nResultados del análisis:")
    for key, value in analysis_results.items():
        print(f"{key}: {value}")

    # Exportar resultados
    analyzer.export_results('output')


if __name__ == "__main__":
    main()