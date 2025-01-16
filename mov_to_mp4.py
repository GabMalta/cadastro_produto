import ffmpeg
import os

def compress_video(input_file, output_file, target_size_mb=20):
    # Define o tamanho máximo em bytes (20MB = 20 * 1024 * 1024)
    target_size = target_size_mb * 1024 * 1024
    
    # Primeira conversão para mp4 sem compressão adicional
    ffmpeg.input(input_file).output(output_file, an=None).run(overwrite_output=True)
    
    # Obtém o tamanho do arquivo de saída
    output_size = os.path.getsize(output_file)
    
    # Se o arquivo for maior que o alvo, reduz a taxa de bitrate
    if output_size > target_size:
        # Calcula um bitrate aproximado necessário para o tamanho desejado
        duration = float(ffmpeg.probe(output_file)['format']['duration'])
        target_bitrate = (target_size * 8) / (duration * 1000)  # em kbps
        
        # Aplica compressão com o bitrate calculado
        ffmpeg.input(input_file).output(
            output_file,
            video_bitrate=f'{target_bitrate}k',
            an=None  # taxa de áudio padrão para qualidade
        ).run(overwrite_output=True)