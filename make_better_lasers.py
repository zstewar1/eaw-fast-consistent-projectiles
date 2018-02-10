from lxml import etree
import traceback


USE_MODEL_BEAMS = False


def is_space_proj(element):
    if element.tag != 'Projectile':
        return False
    if not 'Name' in element.attrib:
        return False
    name = element.attrib['Name']
    return name.startswith('Proj_Ship') or name == 'Proj_Ion_Cannon_Medium_Laser_Blue'

def name(proj):
    return proj.attrib.get('Name')

def update_speed(proj):
    # Set all lasers to double the "normal" laser speed (small lasers were slower) and
    # double the speed of all other projectiles.
    max_speed = proj.find('Max_Speed')
    if max_speed is None:
        return
    speed_value = float(max_speed.text)
    old_speed = speed_value
    if 'Laser' in name(proj) or 'Ion' in name(proj):
        speed_value = 75
    else:
        speed_value *= 2.0
    max_speed.text = f'{speed_value:.1f}'
    print(f'  speed:     {old_speed:>5.1f} -> {speed_value:>5.1f}')

def update_turn(proj):
    # Double the rate of turn of all projectiles -- this should keep their turn radius
    # about the same as it is currently.
    max_turn = proj.find('Max_Rate_Of_Turn')
    if max_turn is None:
        return
    speed_value = float(max_turn.text)
    old_speed = speed_value
    speed_value *= 2.0
    max_turn.text = f'{speed_value:.1f}'
    print(f'  turn rate: {old_speed:>5.1f} -> {speed_value:>5.1f}')

def resize_regular_lasers(proj):
    if not 'Laser' in name(proj):
        return
    custom_render = proj.find('Projectile_Custom_Render')
    if custom_render is None or int(custom_render.text) != 1:
        return
    length = proj.find('Projectile_Length')
    if length is None:
        return
    len_val = float(length.text)
    old_len = len_val
    len_val *= 2.0
    length.text = f'{len_val:.1f}'
    print(f'  length:    {old_len:>5.1f} -> {len_val:>5.1f}')

def change_turbolasers_to_models(proj):
    if not 'Turbolaser' in name(proj):
        return
    if proj.find('Variant_Of_Existing_Type') is not None:
        return
    model = proj.find('Space_Model_Name')
    if model is None:
        model = etree.Element('Space_Model_Name')
        model.tail = '\n\t\t'
        proj.insert(1, model)
    model.text = 'W_LASER_LARGEG.ALO' if 'Green' in name(proj) else 'W_LASER_LARGE.ALO'
    texture_slot = proj.find('Projectile_Texture_Slot')
    texture_slot.text = '3,0' if 'Green' in name(proj) else '0,0'
    custom_render = proj.find('Projectile_Custom_Render')
    custom_render.text = '1'
    print(f'  render: {model.text}')

    width = proj.find('Projectile_Width')
    w = float(width.text)
    old_width = w
    w = w / 5 * 2.5
    width.text = f'{w:.1f}'
    print(f'  width:     {old_width:>5.1f} -> {w:>5.1f}')

    length = proj.find('Projectile_Length')
    l = float(length.text)
    old_len = l
    l *= 5
    length.text = f'{l:.1f}'
    print(f'  length:    {old_len:>5.1f} -> {l:>5.1f}')

def change_ions_to_models(proj):
    if not 'Ion_Cannon' in name(proj) or 'Medium' in name(proj):
        return
    if proj.find('Variant_Of_Existing_Type') is not None:
        return
    model = proj.find('Space_Model_Name')
    if model is None:
        model = etree.Element('Space_Model_Name')
        model.tail = '\n\t\t'
        proj.insert(1, model)
    model.text = 'pion_ioncannonshot.alo'
    texture_slot = proj.find('Projectile_Texture_Slot')
    texture_slot.text = '0,0'
    custom_render = proj.find('Projectile_Custom_Render')
    custom_render.text = '0'
    print(f'  render: {model.text}')

    if 'Small' in name(proj):
        scale_factor = proj.find('Scale_Factor')
        scale_factor.text = '0.25'
        return
        width = proj.find('Projectile_Width')
        w = float(width.text)
        old_width = w
        w *= 0.25
        width.text = f'{w:.1f}'
        print(f'  width:     {old_width:>5.1f} -> {w:>5.1f}')

        length = proj.find('Projectile_Length')
        l = float(length.text)
        old_len = l
        l *= 0.25
        length.text = f'{l:.1f}'
        print(f'  length:    {old_len:>5.1f} -> {l:>5.1f}')

def change_regular_lasers_to_teardrops(proj):
    if not 'Laser' in name(proj):
        return
    custom_render = proj.find('Projectile_Custom_Render')
    if custom_render is not None:
        custom_render.text = '2'
    texture_slot = proj.find('Projectile_Texture_Slot')
    if texture_slot is not None:
        texture_slot.text = '2,0'
    model_name = proj.find('Space_Model_Name')
    if model_name is not None:
        proj.remove(model_name)
    color = proj.find('Projectile_Laser_Color')
    if color is None:
        color = etree.Element('Projectile_Laser_Color')
        color.tail = '\n\t\t'
        proj.insert(1, color)
    color.text = '139,230,104,255' if 'Green' in name(proj) else '238,71,54,255'

    width = proj.find('Projectile_Width')
    if  width is not None:
        w = float(width.text)
        old_width = w
        w = w * 1.2
        width.text = f'{w:.1f}'
        print(f'  width:     {old_width:>5.1f} -> {w:>5.1f}')

    length = proj.find('Projectile_Length')
    if length is not None:
        l = float(length.text)
        old_len = l
        l *= 1.2
        length.text = f'{l:.1f}'
        print(f'  length:    {old_len:>5.1f} -> {l:>5.1f}')

def resize_ions_and_turbos(proj):
    if ('Turbolaser' not in name(proj)
        and ('Ion_Cannon' not in name(proj) or 'Medium' in name(proj))):
        return
    width = proj.find('Projectile_Width')
    if  width is not None:
        w = float(width.text)
        old_width = w
        w = w * 0.7
        width.text = f'{w:.1f}'
        print(f'  width:     {old_width:>5.1f} -> {w:>5.1f}')

    length = proj.find('Projectile_Length')
    if length is not None:
        l = float(length.text)
        old_len = l
        l *= 1.7
        length.text = f'{l:.1f}'
        print(f'  length:    {old_len:>5.1f} -> {l:>5.1f}')

def update_projectile(proj):
    print(f'Updating {name(proj)}')
    update_speed(proj)
    update_turn(proj)
    if USE_MODEL_BEAMS:
        # Change everything to use the laser models
        resize_regular_lasers(proj)
        change_turbolasers_to_models(proj)
        change_ions_to_models(proj)
    else:
        change_regular_lasers_to_teardrops(proj)
        resize_ions_and_turbos(proj)

def main():
    projectiles_file = etree.parse('../Source/Data/XML/projectiles.xml')
    projectiles = projectiles_file.getroot()
    print(projectiles.tag)
    for child in projectiles:
        if is_space_proj(child):
            update_projectile(child)
    projectiles_file.write(
        'Data/XML/projectiles.xml',
        xml_declaration=True,
        encoding=projectiles_file.docinfo.encoding)

if __name__ == '__main__':
    try:
        main()
    except:
        traceback.print_exc()
    input()
