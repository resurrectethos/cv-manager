#!/usr/bin/env python3
"""
CV CLI Tool - Easy command-line interface for managing your CV
"""

import argparse
import json
from datetime import datetime
from cv_generator import CVGenerator


def add_experience(cv: CVGenerator):
    """Interactive prompt to add work experience."""
    print("\n=== Add Work Experience ===")
    company = input("Company name: ")
    position = input("Position title: ")
    start = input("Start date (e.g., 2022 or Jan 2022): ")
    end = input("End date (or 'Present'): ")
    period = f"{start}-{end}"
    
    print("\nEnter responsibilities (one per line, empty line to finish):")
    responsibilities = []
    while True:
        resp = input("- ")
        if not resp:
            break
        responsibilities.append(resp)
    
    experience = {
        "company": company,
        "position": position,
        "period": period,
        "responsibilities": responsibilities
    }
    
    cv.add_experience(experience)
    cv.save_data()
    print(f"\n✓ Added experience at {company}")


def add_publication(cv: CVGenerator):
    """Interactive prompt to add a publication."""
    print("\n=== Add Publication ===")
    print("Type: 1) Book Chapter  2) Conference Proceeding")
    choice = input("Select type (1 or 2): ")
    
    pub_type = "book_chapters" if choice == "1" else "conference_proceedings"
    
    authors = input("Authors (comma-separated, e.g., 'Reddy, P., Pratt, D.'): ")
    authors_list = [a.strip() for a in authors.split(',')]
    
    title = input("Publication title: ")
    year = input("Year: ")
    
    publication = {
        "authors": authors_list,
        "year": int(year),
        "title": title
    }
    
    if pub_type == "book_chapters":
        editors = input("Editors (comma-separated): ")
        publication["editors"] = [e.strip() for e in editors.split(',')]
        publication["book"] = input("Book title: ")
        publication["publisher"] = input("Publisher: ")
    else:
        publication["conference"] = input("Conference name: ")
        publication["location"] = input("Location: ")
        publication["dates"] = input("Dates (e.g., '8-10 July 2025'): ")
        doi = input("DOI (optional, press Enter to skip): ")
        if doi:
            publication["doi"] = doi
    
    cv.add_publication(pub_type, publication)
    cv.save_data()
    print(f"\n✓ Added publication: {title}")


def add_certification(cv: CVGenerator):
    """Interactive prompt to add a certification."""
    print("\n=== Add Certification ===")
    name = input("Certification name: ")
    issuer = input("Issuing organization: ")
    year = int(input("Year obtained: "))
    location = input("Location (optional, press Enter to skip): ")
    
    certification = {
        "name": name,
        "issuer": issuer,
        "year": year
    }
    
    if location:
        certification["location"] = location
    
    cv.add_certification(certification)
    cv.save_data()
    print(f"\n✓ Added certification: {name}")


def update_contact(cv: CVGenerator):
    """Update contact information."""
    print("\n=== Update Contact Information ===")
    print("Leave blank to keep current value")
    
    phone = input(f"Phone [{cv.data['personal_info']['phone']}]: ")
    email = input(f"Email [{cv.data['personal_info']['email']}]: ")
    
    updates = {}
    if phone:
        updates['phone'] = phone
    if email:
        updates['email'] = email
    
    if updates:
        cv.update_section('personal_info', updates)
        cv.save_data()
        print("\n✓ Contact information updated")
    else:
        print("\nNo changes made")


def generate_cv(cv: CVGenerator, args):
    """Generate CV with specified options."""
    print(f"\n=== Generating CV ===")
    print(f"Style: {args.style}")
    print(f"Format: {args.format}")
    
    kwargs = {
        'style': args.style,
        'format': args.format
    }
    
    if args.limit_experience:
        kwargs['experience_limit'] = args.limit_experience
    
    if args.limit_publications:
        kwargs['publications_limit'] = args.limit_publications
    
    if args.sections:
        kwargs['sections'] = args.sections.split(',')
    
    output_file = args.output or f"cv_{args.style}_{datetime.now().strftime('%Y%m%d')}.{args.format.replace('markdown', 'md')}"
    
    cv.save_cv(output_file, **kwargs)
    print(f"\n✓ CV generated: {output_file}")


def show_summary(cv: CVGenerator):
    """Display a summary of the CV data."""
    print("\n=== CV Summary ===")
    print(f"\nName: {cv.data['personal_info']['name']}")
    print(f"Title: {cv.data['personal_info']['title']}")
    print(f"\nEducation entries: {len(cv.data['education'])}")
    print(f"Work experiences: {len(cv.data['work_experience'])}")
    print(f"Certifications: {len(cv.data['certifications'])}")
    print(f"Publications: {len(cv.data['publications']['conference_proceedings']) + len(cv.data['publications']['book_chapters'])}")
    print(f"Professional memberships: {len(cv.data['memberships'])}")
    
    # Show most recent items
    if cv.data['work_experience']:
        recent = cv.data['work_experience'][0]
        print(f"\nMost recent position: {recent['position']} at {recent['company']}")
    
    if cv.data['publications']['conference_proceedings']:
        recent_pub = cv.data['publications']['conference_proceedings'][0]
        print(f"Most recent publication: {recent_pub['title']} ({recent_pub['year']})")


def interactive_menu(cv: CVGenerator):
    """Interactive menu for CV management."""
    while True:
        print("\n" + "="*50)
        print("CV Manager - Interactive Mode")
        print("="*50)
        print("\n1. Add work experience")
        print("2. Add publication")
        print("3. Add certification")
        print("4. Update contact information")
        print("5. Generate CV")
        print("6. Show CV summary")
        print("7. Exit")
        
        choice = input("\nSelect option (1-7): ").strip()
        
        if choice == "1":
            add_experience(cv)
        elif choice == "2":
            add_publication(cv)
        elif choice == "3":
            add_certification(cv)
        elif choice == "4":
            update_contact(cv)
        elif choice == "5":
            print("\nCV Style Options:")
            print("1. Research-focused (full publications)")
            print("2. Industry-focused (technical emphasis)")
            print("3. Academic (comprehensive)")
            print("4. Technical (skills-focused)")
            
            style_choice = input("Select style (1-4): ").strip()
            style_map = {"1": "research", "2": "industry", "3": "academic", "4": "technical"}
            style = style_map.get(style_choice, "research")
            
            format_choice = input("Format (markdown/html) [markdown]: ").strip() or "markdown"
            
            # Create a minimal args object
            class Args:
                pass
            args = Args()
            args.style = style
            args.format = format_choice
            args.output = None
            args.limit_experience = None
            args.limit_publications = None
            args.sections = None
            
            generate_cv(cv, args)
        elif choice == "6":
            show_summary(cv)
        elif choice == "7":
            print("\nGoodbye!")
            break
        else:
            print("\n❌ Invalid option. Please try again.")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="CV Manager - Generate and update your CV easily",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode
  python cv_cli.py -i

  # Generate a research-focused CV
  python cv_cli.py generate -s research -f markdown

  # Generate industry CV with limited entries
  python cv_cli.py generate -s industry -f html --limit-exp 3

  # Add new experience
  python cv_cli.py add experience

  # Show CV summary
  python cv_cli.py summary
        """
    )
    
    parser.add_argument('-i', '--interactive', action='store_true',
                       help='Run in interactive mode')
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Generate command
    gen_parser = subparsers.add_parser('generate', help='Generate CV')
    gen_parser.add_argument('-s', '--style', 
                           choices=['research', 'industry', 'academic', 'technical'],
                           default='research',
                           help='CV style/focus')
    gen_parser.add_argument('-f', '--format',
                           choices=['markdown', 'html'],
                           default='markdown',
                           help='Output format')
    gen_parser.add_argument('-o', '--output',
                           help='Output filename')
    gen_parser.add_argument('--limit-exp', '--limit-experience',
                           type=int, dest='limit_experience',
                           help='Limit number of work experiences')
    gen_parser.add_argument('--limit-pub', '--limit-publications',
                           type=int, dest='limit_publications',
                           help='Limit number of publications')
    gen_parser.add_argument('--sections',
                           help='Comma-separated list of sections to include')
    
    # Add commands
    add_parser = subparsers.add_parser('add', help='Add new entry')
    add_parser.add_argument('type',
                           choices=['experience', 'publication', 'certification'],
                           help='Type of entry to add')
    
    # Update command
    update_parser = subparsers.add_parser('update', help='Update existing data')
    update_parser.add_argument('section',
                              choices=['contact'],
                              help='Section to update')
    
    # Summary command
    subparsers.add_parser('summary', help='Show CV summary')
    
    args = parser.parse_args()
    
    # Initialize CV generator
    cv = CVGenerator()
    
    # Handle commands
    if args.interactive:
        interactive_menu(cv)
    elif args.command == 'generate':
        generate_cv(cv, args)
    elif args.command == 'add':
        if args.type == 'experience':
            add_experience(cv)
        elif args.type == 'publication':
            add_publication(cv)
        elif args.type == 'certification':
            add_certification(cv)
    elif args.command == 'update':
        if args.section == 'contact':
            update_contact(cv)
    elif args.command == 'summary':
        show_summary(cv)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
    