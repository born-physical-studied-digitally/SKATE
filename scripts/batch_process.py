#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch processing script for seismogram pipeline.

Description:
  Process multiple seismogram images in batch, generating all metadata
  (ROI, meanlines, intersections, and segments) for each image.

Usage:
  batch_process.py --input-dir <directory> --output-dir <directory> [--pattern <pattern>] [--stats <filename>] [--scale <scale>] [--debug <directory>] [--fix-seed] [--max-workers <number>]
  batch_process.py -h | --help

Options:
  -h --help                    Show this screen.
  --input-dir <directory>      Directory containing input images.
  --output-dir <directory>     Base directory to save metadata outputs.
  --pattern <pattern>          File pattern to match (e.g., "*.png", "*.jpg") [default: "*.png"]
  --stats <filename>           Write statistics to <filename>.
  --scale <scale>              1 for a full-size seismogram, 0.25 for quarter-size, etc. [default: 1]
  --debug <directory>          Save intermediate steps as images for inspection in <directory>.
  --fix-seed                   Fix random seed.
  --max-workers <number>       Maximum number of parallel workers [default: 1]

Examples:
  batch_process.py --input-dir ./data/inputs --output-dir ./data/outputs --pattern "*.png"
  batch_process.py --input-dir ./data/inputs --output-dir ./data/outputs --pattern "*.jpg" --max-workers 4
"""

import os
import sys
import glob
import time
import argparse
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
import traceback

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from seismogram_pipeline.cli.get_all_metadata import analyze_image
from seismogram_pipeline.core.dir import ensure_dir_exists


def process_single_file(args):
    """Process a single file with the given arguments."""
    input_file, output_dir, stats_file, scale, debug_dir, fix_seed = args
    
    try:
        print(f"Processing: {input_file}")
        start_time = time.time()
        
        # Process the image
        analyze_image(
            in_file=input_file,
            out_dir=output_dir,
            stats_file=stats_file,
            scale=scale,
            debug_dir=debug_dir,
            fix_seed=fix_seed
        )
        
        elapsed_time = time.time() - start_time
        print(f"Completed: {input_file} (took {elapsed_time:.2f}s)")
        
        return {
            'file': input_file,
            'status': 'success',
            'elapsed_time': elapsed_time
        }
        
    except Exception as e:
        print(f"Error processing {input_file}: {str(e)}")
        traceback.print_exc()
        return {
            'file': input_file,
            'status': 'error',
            'error': str(e)
        }


def main():
    """Main entry point for batch processing."""
    parser = argparse.ArgumentParser(
        description="Batch process multiple seismogram images",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument('--input-dir', required=True,
                       help='Directory containing input images')
    parser.add_argument('--output-dir', required=True,
                       help='Base directory to save metadata outputs')
    parser.add_argument('--pattern', default='*.png',
                       help='File pattern to match (e.g., "*.png", "*.jpg") [default: "*.png"]')
    parser.add_argument('--stats',
                       help='Write statistics to filename')
    parser.add_argument('--scale', type=float, default=1.0,
                       help='Scale factor (1 for full-size, 0.25 for quarter-size, etc.) [default: 1]')
    parser.add_argument('--debug',
                       help='Save intermediate steps as images for inspection in directory')
    parser.add_argument('--fix-seed', action='store_true',
                       help='Fix random seed')
    parser.add_argument('--max-workers', type=int, default=1,
                       help='Maximum number of parallel workers [default: 1]')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input_dir):
        print(f"Error: Input directory '{args.input_dir}' does not exist.")
        sys.exit(1)
    
    ensure_dir_exists(args.output_dir)
    
    pattern = os.path.join(args.input_dir, args.pattern)
    input_files = glob.glob(pattern)
    
    if not input_files:
        print(f"No files found matching pattern '{pattern}'")
        sys.exit(1)
    
    print(f"Found {len(input_files)} files to process:")
    for f in input_files:
        print(f"  {f}")
    print()
    
    file_args = []
    for input_file in input_files:
        filename = os.path.basename(input_file)
        name_without_ext = os.path.splitext(filename)[0]
        file_output_dir = os.path.join(args.output_dir, name_without_ext)
        
        stats_file = None
        if args.stats:
            stats_base = os.path.splitext(args.stats)[0]
            stats_ext = os.path.splitext(args.stats)[1]
            stats_file = f"{stats_base}_{name_without_ext}{stats_ext}"
        
        # Prepare debug directory if specified
        debug_dir = None
        if args.debug:
            debug_dir = os.path.join(args.debug, name_without_ext)
        
        file_args.append((
            input_file,
            file_output_dir,
            stats_file,
            args.scale,
            debug_dir,
            args.fix_seed
        ))
    
    start_time = time.time()
    results = []
    
    if args.max_workers == 1:
        print("Processing files sequentially...")
        for file_arg in file_args:
            result = process_single_file(file_arg)
            results.append(result)
    else:

        print(f"Processing files with {args.max_workers} workers...")
        with ProcessPoolExecutor(max_workers=args.max_workers) as executor:

            future_to_file = {
                executor.submit(process_single_file, file_arg): file_arg[0]
                for file_arg in file_args
            }
            
            for future in as_completed(future_to_file):
                result = future.result()
                results.append(result)
    
    total_time = time.time() - start_time
    successful = sum(1 for r in results if r['status'] == 'success')
    failed = sum(1 for r in results if r['status'] == 'error')
    
    print(f"\n{'='*50}")
    print(f"BATCH PROCESSING SUMMARY")
    print(f"{'='*50}")
    print(f"Total files processed: {len(results)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Total time: {total_time:.2f}s")
    print(f"Average time per file: {total_time/len(results):.2f}s")
    
    if failed > 0:
        print(f"\nFailed files:")
        for result in results:
            if result['status'] == 'error':
                print(f"  {result['file']}: {result['error']}")
    
    if successful > 0:
        print(f"\nSuccessful files:")
        for result in results:
            if result['status'] == 'success':
                print(f"  {result['file']} ({result['elapsed_time']:.2f}s)")


if __name__ == '__main__':
    main() 