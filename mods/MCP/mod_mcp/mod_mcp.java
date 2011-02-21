package MCP.mod_mcp;

import org.lwjgl.input.Keyboard;

import MCP.ApiController;
import MCP.ApiCraftMgr;
import MCP.Mod;
import net.minecraft.src.Block;
import net.minecraft.src.Entity;
import net.minecraft.src.EntityChicken;
import net.minecraft.src.EntityPlayer;
import net.minecraft.src.Item;
import net.minecraft.src.ItemStack;
import net.minecraft.src.Material;

public class mod_mcp extends Mod
{
	private long tickCounter;
	private ItemSilverOre silverOre;
	private ItemSilver silver;
	private ItemScepter scepter;
	
	/**********************************************************************
	 * 
	 */
	public mod_mcp(ApiController ctrl)
	{
		super(ctrl);
	}
	
	/**********************************************************************
	 * 
	 */
	@Override
	public String getModName()
	{
		return "MCP Test Mod";
	}

	/**********************************************************************
	 * 
	 */
	@Override
	public String getModAuthor()
	{
		return "Searge";
	}

	/**********************************************************************
	 * 
	 */
	@Override
	public String getModDescription()
	{
		String desc = "Add a recipe to create string from cloth.";
		desc += "\nUsing the mod system recipe manager.";
		return desc;
	}

	/**********************************************************************
	 * 
	 */
	@Override
	public void onMinecraftStarted()
	{
	}

	/**********************************************************************
	 * 
	 */
	@Override
	public void onMinecraftEnding()
	{
	}

	/**********************************************************************
	 * 
	 */
	@Override
	public void onGameStarted()
	{
		this.tickCounter = 1;
	}

	/**********************************************************************
	 * 
	 */
	@Override
	public void onGameEnding()
	{
		this.tickCounter = 0;
	}
	
	/**********************************************************************
	 * 
	 */
	@Override
	public void onTick()
	{
		if(this.tickCounter > 0)
			++this.tickCounter;

		if(this.tickCounter == 10)
			api().printc("\2477Press 't' to open the console and enter /help for more info");
		
		if(this.tickCounter == 90)
		{
			api().printc("\247cSearge\247e mod system v1.0");
			api().printc("\247aWelcome to \247cmod_mcp\247a. \247eHave fun.");
		}
	}

	/**********************************************************************
	 * 
	 */
	@Override
	public void onRegisterBlocksAndItems()
	{
		int silverIcon = api().registerItemIcon(imageName(getClass(), "gfx/mcp.png"), 0);
		int silverTexture = api().registerBlockTexture(imageName(getClass(), "gfx/mcp.png"), 1);
		int scepterIcon = api().registerItemIcon(imageName(getClass(), "gfx/mcp.png"), 2);
		
		this.silverOre = new ItemSilverOre(api(), silverTexture, Material.iron, BlockSilverOre.class);
		this.silver = new ItemSilver(api(), silverIcon);
		this.scepter = new ItemScepter(api(), scepterIcon);
	}

	/**********************************************************************
	 * 
	 */
	@Override
	public void onRegisterRecipes(ApiCraftMgr craftMgr)
	{
        craftMgr.addShapelessRecipe(new ItemStack(Item.silk, 4), new Object[] {
            Block.cloth
        });

        craftMgr.addFurnaceRecipe(this.silverOre, new ItemStack(this.silver));
        
        craftMgr.addRecipe(new ItemStack(this.scepter), new Object[] {
            "  #", " / ", "/  ", Character.valueOf('#'), Item.diamond, Character.valueOf('/'), this.silver
        });
        
        //*DEBUG:
        craftMgr.addRecipe(new ItemStack(this.silverOre, 4), new Object[] {
            "# #", " # ", "# #", Character.valueOf('#'), Item.diamond
        });
        
        craftMgr.addRecipe(new ItemStack(Item.diamond, 8), new Object[] {
            " #", "# ", Character.valueOf('#'), Block.sand
        });
        
        craftMgr.addRecipe(new ItemStack(Item.flintAndSteel, 1), new Object[] {
            " #", "# ", Character.valueOf('#'), Block.dirt
        });
        
        craftMgr.addRecipe(new ItemStack(Block.obsidian, 10), new Object[] {
            "##", " #", Character.valueOf('#'), Block.sand
        });
        
        craftMgr.addRecipe(new ItemStack(Block.wood, 8), new Object[] {
            "##", " #", Character.valueOf('#'), Block.dirt
        });
        //*/
	}
	
	/**********************************************************************
	 * 
	 */
	@Override
	public boolean onConsoleCommand(String command, String param)
	{
		if(command.equals("help"))
		{
			api().printc("Try /hello");
			return true;
		}
		if(command.equals("hello"))
		{
			api().printc("Hello " + api().mc().session.username);
			return true;
		}
		
		return false;
	}

	/**********************************************************************
	 * 
	 */
	@Override
	public boolean onKeyPress(int keycode, boolean pressed)
	{
		if(pressed)
		{
			switch(keycode)
			{
				case Keyboard.KEY_HOME:
					api().mc().theWorld.worldTime = 0;
					return true;
				case Keyboard.KEY_END:
					api().mc().theWorld.worldTime = 12000;
					return true;
			}
		}
		return false;
	}

	/**********************************************************************
	 * 
	 */
	@Override
	public int onAddFuel(int itemID)
	{
		if(itemID == Block.cloth.blockID)
			return 1000;
		if(itemID == Item.dyePowder.shiftedIndex)
			return 500;
			
		return 0;
	}

	/**********************************************************************
	 * 
	 */
	@Override
	public boolean onEntityLeftClick(EntityPlayer player, Entity entity, ItemStack withItem)
	{
		if(withItem != null && withItem.getItem() == this.scepter && entity instanceof EntityChicken)
		{
			entity.dropItem(Item.egg.shiftedIndex, 1);
			return true;
		}
		
		return false;
	}
	
	/**********************************************************************
	 * 
	 */
	@Override
	public boolean onEntityRightClick(EntityPlayer player, Entity entity, ItemStack withItem)
	{
		if(withItem != null && withItem.getItem() == this.scepter && entity instanceof EntityChicken)
		{
			entity.dropItem(Item.feather.shiftedIndex, 1);
			return true;
		}
		
		return false;
	}

	/**********************************************************************
	 * 
	 */
	@Override
	public boolean onBlockLeftClick(EntityPlayer player, Block block, int x, int y, int z, int side, ItemStack withItem)
	{
		if(withItem != null && withItem.getItem() == this.scepter && (block == Block.sand || block == Block.blockGold))
		{
			api().mc().theWorld.setBlockWithNotify(x, y, z, Block.blockGold.blockID);
			return true;
		}
		
		return false;
	}
	
	/**********************************************************************
	 * 
	 */
	@Override
	public boolean onBlockRightClick(EntityPlayer player, Block block, int x, int y, int z, int side, ItemStack withItem)
	{
		if(withItem != null && withItem.getItem() == this.scepter && (block == Block.sand || block == Block.blockDiamond))
		{
			api().mc().theWorld.setBlockWithNotify(x, y, z, Block.blockDiamond.blockID);
			return true;
		}
		
		return false;
	}
}
